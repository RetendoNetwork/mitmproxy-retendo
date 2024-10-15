from mitmproxy import http, ctx

class RetendoAddon:
    def load(self, loader) -> None:
        loader.add_option(
            name="retendo_redirect",
            typespec=bool,
            default=True,
            help="Redirect all requests from Nintendo to Retendo",
        )

        loader.add_option(
            name="retendo_host",
            typespec=str,
            default="",
            help="Host to send Retendo requests to (keeps the original host in the Host header)",
        )

        loader.add_option(
            name="retendo_host_port",
            typespec=int,
            default=80,
            help="Port to send Retendo requests to (only applies if retendo_host is set)",
        )

        loader.add_option(
            name="retendo_http",
            typespec=bool,
            default=False,
            help="Sets Retendo requests to HTTP (only applies if retendo_host is set)",
        )

    def request(self, flow: http.HTTPFlow) -> None:
        if ctx.options.retendo_redirect:
            if "nintendo.net" in flow.request.pretty_host:
                flow.request.host = flow.request.pretty_host.replace(
                    "nintendo.net", "retendo.online"
                )
            elif "nintendowifi.net" in flow.request.pretty_host:
                flow.request.host = flow.request.pretty_host.replace(
                    "nintendowifi.net", "retendo.online"
                )

            if ctx.options.retendo_host and (
                "retendo.online" in flow.request.pretty_host
                or "retendo.online" in flow.request.pretty_host
                or "cdn.retendo.online" in flow.request.pretty_host
            ):
                original_host = flow.request.host_header
                flow.request.host = ctx.options.retendo_host
                flow.request.port = ctx.options.retendo_host_port
                flow.request.host_header = original_host

                if ctx.options.retendo_http:
                    flow.request.scheme = "http"


addons = [RetendoAddon()]
