from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Update domains for temp mail"

    def handle(self, *args, **options):
        from apps.temp_mail.models import Domain
        from apps.temp_mail.scrapping.scrapping import TempMail as TempMailScrapping

        mail_scrapping = TempMailScrapping()
        domains = mail_scrapping.get_all_domains()["email_domain"]
        if not domains:
            raise Exception("Domains not found")
        data = []
        for domain in domains:
            data.append(Domain(domain=domain))
        Domain.objects.bulk_create(data, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("Successfully updated domains"))
