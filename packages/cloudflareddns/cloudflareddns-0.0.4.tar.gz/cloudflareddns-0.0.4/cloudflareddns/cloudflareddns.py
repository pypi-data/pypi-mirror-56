#!/usr/bin/env python

import argparse
import logging as log  # for verbose output
import os
import socket  # to get default hostname
import sys

import CloudFlare
import tldextract
from CloudFlare.exceptions import CloudFlareAPIError

from .__about__ import __version__


def update(cfUsername, cfKey, hostname, ip, ttl=None):
    """
    Create or update desired DNS record.
    Returns Synology-friendly status strings:
    https://community.synology.com/enu/forum/17/post/57640?reply=213305
    """
    log.debug("Updating {} to {}".format(hostname, ip))

    # get zone name correctly (from hostname)
    zoneDomain = tldextract.extract(hostname).registered_domain
    log.debug("Zone domain of hostname is {}".format(zoneDomain))

    if ':' in ip:
        ipAddressType = 'AAAA'
    else:
        ipAddressType = 'A'

    cf = CloudFlare.CloudFlare(email=cfUsername, token=cfKey)
    # now get the zone id
    try:
        params = {'name': zoneDomain}
        zones = cf.zones.get(params=params)
    except CloudFlareAPIError as e:
        log.error('Bad auth - %s' % e)
        return 'badauth'
    except Exception as e:
        log.error('/zones.get - %s - api call failed' % e)
        return '911'

    if len(zones) == 0:
        log.error('No host')
        return 'nohost'

    if len(zones) != 1:
        log.error('/zones.get - %s - api call returned %d items' % (zoneDomain, len(zones)))
        return 'notfqdn'

    zone_id = zones[0]['id']
    log.debug("Zone ID is {}".format(zone_id))

    try:
        params = {'name': hostname, 'match': 'all', 'type': ipAddressType}
        dns_records = cf.zones.dns_records.get(zone_id, params=params)
    except CloudFlareAPIError as e:
        log.error('/zones/dns_records %s - %d %s - api call failed' % (hostname, e, e))
        return '911'

    desiredRecordData = {
        'name': hostname,
        'type': ipAddressType,
        'content': ip
    }
    if ttl:
        desiredRecordData['ttl'] = ttl

    # update the record - unless it's already correct
    for dnsRecord in dns_records:
        oldIp = dnsRecord['content']
        oldIpType = dnsRecord['type']

        if ipAddressType not in ['A', 'AAAA']:
            # we only deal with A / AAAA records
            continue

        if ipAddressType != oldIpType:
            # only update the correct address type (A or AAAA)
            # we don't see this becuase of the search params above
            log.debug('IGNORED: %s %s ; wrong address family' % (hostname, oldIp))
            continue

        if ip == oldIp:
            log.info('UNCHANGED: %s == %s' % (hostname, ip))
            # nothing to do, record already matches to desired IP
            return 'nochg'

        # Yes, we need to update this record - we know it's the same address type
        dnsRecordId = dnsRecord['id']

        try:
            cf.zones.dns_records.put(zone_id, dnsRecordId, data=desiredRecordData)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            log.error('/zones.dns_records.put %s - %d %s - api call failed' % (hostname, e, e))
            return '911'
        log.info('UPDATED: %s %s -> %s' % (hostname, oldIp, ip))
        return 'good'

    # no exsiting dns record to update - so create dns record
    try:
        cf.zones.dns_records.post(zone_id, data=desiredRecordData)
        log.info('CREATED: %s %s' % (hostname, ip))
        return 'good'
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        log.error('/zones.dns_records.post %s - %d %s - api call failed' % (hostname, e, e))
        return '911'

    # reached far enough without genuine return/exception catching, must be an error
    # using 'badagent' just because it is unique to other statuses used above
    return 'badagent'


def updateRecord(hostname, ip, ttl=None):
    res = update(os.environ['CF_EMAIL'], os.environ['CF_KEY'], hostname, ip, ttl)
    return res in ['good', 'nochg']


def main():
    parser = argparse.ArgumentParser(description='Update DDNS in Cloudflare.')
    parser.add_argument('--email', help='Cloudflare account emai')
    parser.add_argument('--key', help='Cloudflare API key')
    parser.add_argument('--hostname', metavar='HOSTNAME',
                        help='Hostname to set IP for')
    parser.add_argument('--ip', dest='ip',
                        help='The IP address')
    parser.add_argument('--ttl', type=int, help='TTL in seconds')
    parser.add_argument('--verbose', dest='verbose', action='store_true')

    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    parser.set_defaults(hostname=socket.getfqdn(), ttl=None, email=os.environ['CF_EMAIL'],
                        key=os.environ['CF_KEY'])

    args = parser.parse_args()

    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.debug("Verbose output.")
    else:
        log.basicConfig(format="%(message)s", level=log.INFO)

    update(args.email, args.key, args.hostname, args.ip, args.ttl)


def syno():
    """
    In Synology wrapper, we echo the return value of the "update" for users to see errors:
    """
    print(update(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 120))


if __name__ == '__main__':
    main()
