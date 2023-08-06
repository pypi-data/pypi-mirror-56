from prometheus_client.core import GaugeMetricFamily

import CloudFlare


class CloudflareCollector:
    def __init__(self, cloudflare_token):
        self.cloudflare_token = cloudflare_token

    def collect(self):
        families = {
            'received_requests': GaugeMetricFamily(
                'cloudflare_pop_received_requests',
                'Requests received at this PoP location.',
                labels=['zone', 'type', 'colo_id'],
            ),
            'bandwidth_bytes': GaugeMetricFamily(
                'cloudflare_pop_bandwidth_bytes',
                'Bandwidth used from this PoP location.',
                labels=['zone', 'type', 'colo_id'],
            ),
            'http_responses_sent': GaugeMetricFamily(
                'cloudflare_pop_http_responses_sent',
                'Breakdown per HTTP response code.',
                labels=['zone', 'colo_id', 'http_status'],
            ),
            'threats_seen': GaugeMetricFamily(
                'cloudflare_pop_threats_seen',
                'Threats identified.',
                labels=['zone', 'colo_id', 'threats'],
            ),
            'threat_types': GaugeMetricFamily(
                'cloudflare_pop_threat_types',
                'Threat breakdown per threat type.',
                labels=['zone', 'colo_id', 'threat_type'],
            ),
            'threat_countries': GaugeMetricFamily(
                'cloudflare_pop_threat_countries',
                'Threat breakdown per country.',
                labels=['zone', 'colo_id', 'threat_country'],
            ),
        }
        for zone, raw_data in _get_cloudflare_analytics(self.cloudflare_token):
            # We're interested in the latest metrics, however
            # the Cloudflare API doesn't guarantee non-zero values.
            # Index -2 was chosen empirically and is usually non-zero.
            for pop_data in raw_data:
                serie = pop_data['timeseries'][-2]

                families['received_requests'].add_metric(
                    [zone, 'cached', pop_data['colo_id']], serie['requests']['cached']
                )
                families['received_requests'].add_metric(
                    [zone, "uncached", pop_data["colo_id"]], serie["requests"]["uncached"]
                )

                families["bandwidth_bytes"].add_metric(
                    [zone, "cached", pop_data['colo_id']], serie['bandwidth']['cached']
                )
                families['bandwidth_bytes'].add_metric(
                    [zone, 'uncached', pop_data['colo_id']], serie['bandwidth']['uncached']
                )

                for http_status, count in serie["requests"]["http_status"].items():
                    families['http_responses_sent'].add_metric(
                        [zone, pop_data["colo_id"], http_status], count
                    )

                families['threats_seen'].add_metric(
                    [zone, pop_data['colo_id']], serie['threats']['all']
                )

                for threat, count in serie['threats']['type'].items():
                    families['threat_types'].add_metric(
                        [zone, pop_data['colo_id'], threat], count
                    )

                for country, count in serie['threats']['country'].items():
                    families['threat_countries'].add_metric(
                        [zone, pop_data['colo_id'], country], count
                    )

                for metric in families.values():
                    yield metric


def _get_cloudflare_analytics(token):
    cloudflare = CloudFlare.CloudFlare(debug=False, token=token)
    for zone in cloudflare.zones.get():
        # get the last 30 minutes (the very last 5 minutes are usually not correct)
        series = cloudflare.zones.analytics.colos(zone['id'], params={'since': -35, 'until': -5})
        yield zone['name'], series
