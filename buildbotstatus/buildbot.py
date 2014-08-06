import httplib
import json

def get_json(url, node, method="GET"):
    conn = httplib.HTTPConnection(url)
    try:
        conn.request(method, node)
        r = conn.getresponse()
        if r.status != 200:
            raise Exception("Server response for %s/%s: %s %s" %
                    (url, node, r.status, r.reason))
        data = r.read()
        return json.loads(data)
    finally:
        conn.close()

def get_builders(url):
    return get_json(url, "/json/builders")

def get_build(url, name, num):
    return get_json(url, "/json/builders/%s/builds/%s" % (name, num))

def get_build_property(build, propname):
    properties = build['properties']
    for prop in properties:
        if prop[0] == propname:
            return prop[1]
    return None

def find_builds(url, revision):
    builders = get_builders(url)
    matching = []
    for (name,builder) in builders.iteritems():
        builds = builder['cachedBuilds']
        builds.reverse()
        for buildnum in builds:
            build = get_build(url, name, buildnum)
            got_rev = get_build_property(build, 'got_revision')
            if got_rev == revision:
                matching.append(build)
                break
    return matching
