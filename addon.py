from mitmproxy import http, ctx
import re

class Addon:
    def load(self, loader) -> None:
        loader.add_option(name="retendo_redirect", typespec=bool, default=True, help="Redirect Nintendo to Retendo")
        loader.add_option(name="retendo_host", typespec=str, default="", help="Host for Pretendo requests")
        loader.add_option(name="retendo_host_port", typespec=int, default=80, help="Port for Pretendo requests")
        loader.add_option(name="retendo_http", typespec=bool, default=False, help="Use HTTP for Pretendo requests")

        self.nintendo_patterns = [
            re.compile(r".*nintendo\.net$"),
            re.compile(r".*nintendowifi\.net$"),
            re.compile(r".*switch-online\.com$"),
            re.compile(r".*e\.shop\.nintendo\.net$")
        ]

    def request(self, flow: http.HTTPFlow) -> None:
        if ctx.options.retendo_redirect and any(p.match(flow.request.pretty_host) for p in self.nintendo_patterns):
            ctx.log.info(f"Redirecting: {flow.request.pretty_host} -> pretendo.cc")
            flow.request.host = "retendo.online"

            if ctx.options.retendo_host:
                original_host = flow.request.host_header
                flow.request.host = ctx.options.retendo_host
                flow.request.port = ctx.options.retendo_host_port
                flow.request.host_header = original_host

                if ctx.options.retendo_http and flow.request.scheme == "https":
                    flow.request.scheme = "http"

addons = [Addon()]
