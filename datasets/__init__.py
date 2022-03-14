def __init__(self, domain, **kwargs):
    self.allowed_domains = [f'{domain}']
    self.start_urls = [f'https://{domain}']
    super().__init__(**kwargs)