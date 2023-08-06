from conapp.definitions import Hosts


def get_bitbucket_url(user: str, repo: str = "config", commit: str = "master") -> str:
    return f"https://bitbucket.org/{user}/{repo}/get/{commit}.tar.gz"


def get_github_url(user: str, repo: str = "config", commit: str = "master") -> str:
    return f"https://github.com/{user}/{repo}/tarball/{commit}"


RESOLVERS = {
    Hosts.GITHUB: get_github_url,
    Hosts.BITBUCKET: get_bitbucket_url
}


def get_bitbucket_checkout_url(user: str, repo: str = "config") -> str:
    return f"https://bitbucket.org/{user}/{repo}.git"


def get_github_checkout_url(user: str, repo: str = "config") -> str:
    return f"https://github.com/{user}/{repo}.git"


CHECKOUT_RESOLVERS = {
    Hosts.GITHUB: get_github_checkout_url,
    Hosts.BITBUCKET: get_bitbucket_checkout_url,
}
