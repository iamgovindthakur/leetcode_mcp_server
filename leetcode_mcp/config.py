import os


class Settings:
    """Lightweight settings object that reads from environment variables.

    This avoids a hard dependency on `pydantic.BaseSettings` and works in
    environments with different pydantic versions.
    """

    def __init__(self):
        self.user_agent = os.getenv(
            "LC_USER_AGENT",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122 Safari/537.36",
        )
        # allow overriding timeout via LC_TIMEOUT (seconds)
        try:
            self.timeout = float(os.getenv("LC_TIMEOUT", "10.0"))
        except ValueError:
            self.timeout = 10.0


settings = Settings()
