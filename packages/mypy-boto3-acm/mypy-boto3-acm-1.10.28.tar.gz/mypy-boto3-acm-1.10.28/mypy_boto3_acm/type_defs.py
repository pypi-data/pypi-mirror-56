"Main interface for acm type defs"
from __future__ import annotations

from datetime import datetime
from typing import List
from typing_extensions import TypedDict


__all__ = (
    "CertificateValidatedWaitWaiterConfigTypeDef",
    "ClientAddTagsToCertificateTagsTypeDef",
    "ClientDescribeCertificateResponseCertificateDomainValidationOptionsResourceRecordTypeDef",
    "ClientDescribeCertificateResponseCertificateDomainValidationOptionsTypeDef",
    "ClientDescribeCertificateResponseCertificateExtendedKeyUsagesTypeDef",
    "ClientDescribeCertificateResponseCertificateKeyUsagesTypeDef",
    "ClientDescribeCertificateResponseCertificateOptionsTypeDef",
    "ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsResourceRecordTypeDef",
    "ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsTypeDef",
    "ClientDescribeCertificateResponseCertificateRenewalSummaryTypeDef",
    "ClientDescribeCertificateResponseCertificateTypeDef",
    "ClientDescribeCertificateResponseTypeDef",
    "ClientExportCertificateResponseTypeDef",
    "ClientGetCertificateResponseTypeDef",
    "ClientImportCertificateResponseTypeDef",
    "ClientImportCertificateTagsTypeDef",
    "ClientListCertificatesIncludesTypeDef",
    "ClientListCertificatesResponseCertificateSummaryListTypeDef",
    "ClientListCertificatesResponseTypeDef",
    "ClientListTagsForCertificateResponseTagsTypeDef",
    "ClientListTagsForCertificateResponseTypeDef",
    "ClientRemoveTagsFromCertificateTagsTypeDef",
    "ClientRequestCertificateDomainValidationOptionsTypeDef",
    "ClientRequestCertificateOptionsTypeDef",
    "ClientRequestCertificateResponseTypeDef",
    "ClientRequestCertificateTagsTypeDef",
    "ClientUpdateCertificateOptionsOptionsTypeDef",
    "ListCertificatesPaginateIncludesTypeDef",
    "ListCertificatesPaginatePaginationConfigTypeDef",
    "ListCertificatesPaginateResponseCertificateSummaryListTypeDef",
    "ListCertificatesPaginateResponseTypeDef",
)


_CertificateValidatedWaitWaiterConfigTypeDef = TypedDict(
    "_CertificateValidatedWaitWaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)


class CertificateValidatedWaitWaiterConfigTypeDef(_CertificateValidatedWaitWaiterConfigTypeDef):
    """
    Type definition for `CertificateValidatedWait` `WaiterConfig`

    A dictionary that provides parameters to control waiting behavior.

    - **Delay** *(integer) --*

      The amount of time in seconds to wait between attempts. Default: 60

    - **MaxAttempts** *(integer) --*

      The maximum number of attempts to be made. Default: 40
    """


_RequiredClientAddTagsToCertificateTagsTypeDef = TypedDict(
    "_RequiredClientAddTagsToCertificateTagsTypeDef", {"Key": str}
)
_OptionalClientAddTagsToCertificateTagsTypeDef = TypedDict(
    "_OptionalClientAddTagsToCertificateTagsTypeDef", {"Value": str}, total=False
)


class ClientAddTagsToCertificateTagsTypeDef(
    _RequiredClientAddTagsToCertificateTagsTypeDef, _OptionalClientAddTagsToCertificateTagsTypeDef
):
    """
    Type definition for `ClientAddTagsToCertificate` `Tags`

    A key-value pair that identifies or specifies metadata about an ACM resource.

    - **Key** *(string) --* **[REQUIRED]**

      The key of the tag.

    - **Value** *(string) --*

      The value of the tag.
    """


_ClientDescribeCertificateResponseCertificateDomainValidationOptionsResourceRecordTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateDomainValidationOptionsResourceRecordTypeDef",
    {"Name": str, "Type": str, "Value": str},
    total=False,
)


class ClientDescribeCertificateResponseCertificateDomainValidationOptionsResourceRecordTypeDef(
    _ClientDescribeCertificateResponseCertificateDomainValidationOptionsResourceRecordTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponseCertificateDomainValidationOptions`
    `ResourceRecord`

    Contains the CNAME record that you add to your DNS database for domain validation. For more
    information, see `Use DNS to Validate Domain Ownership
    <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

    - **Name** *(string) --*

      The name of the DNS record to create in your domain. This is supplied by ACM.

    - **Type** *(string) --*

      The type of DNS record. Currently this can be ``CNAME`` .

    - **Value** *(string) --*

      The value of the CNAME record to add to your DNS database. This is supplied by ACM.
    """


_ClientDescribeCertificateResponseCertificateDomainValidationOptionsTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateDomainValidationOptionsTypeDef",
    {
        "DomainName": str,
        "ValidationEmails": List[str],
        "ValidationDomain": str,
        "ValidationStatus": str,
        "ResourceRecord": ClientDescribeCertificateResponseCertificateDomainValidationOptionsResourceRecordTypeDef,
        "ValidationMethod": str,
    },
    total=False,
)


class ClientDescribeCertificateResponseCertificateDomainValidationOptionsTypeDef(
    _ClientDescribeCertificateResponseCertificateDomainValidationOptionsTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponseCertificate` `DomainValidationOptions`

    Contains information about the validation of each domain name in the certificate.

    - **DomainName** *(string) --*

      A fully qualified domain name (FQDN) in the certificate. For example, ``www.example.com`` or
      ``example.com`` .

    - **ValidationEmails** *(list) --*

      A list of email addresses that ACM used to send domain validation emails.

      - *(string) --*

    - **ValidationDomain** *(string) --*

      The domain name that ACM used to send domain validation emails.

    - **ValidationStatus** *(string) --*

      The validation status of the domain name. This can be one of the following values:

      * ``PENDING_VALIDATION``

      * SUCCESS

      * FAILED

    - **ResourceRecord** *(dict) --*

      Contains the CNAME record that you add to your DNS database for domain validation. For more
      information, see `Use DNS to Validate Domain Ownership
      <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

      - **Name** *(string) --*

        The name of the DNS record to create in your domain. This is supplied by ACM.

      - **Type** *(string) --*

        The type of DNS record. Currently this can be ``CNAME`` .

      - **Value** *(string) --*

        The value of the CNAME record to add to your DNS database. This is supplied by ACM.

    - **ValidationMethod** *(string) --*

      Specifies the domain validation method.
    """


_ClientDescribeCertificateResponseCertificateExtendedKeyUsagesTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateExtendedKeyUsagesTypeDef",
    {"Name": str, "OID": str},
    total=False,
)


class ClientDescribeCertificateResponseCertificateExtendedKeyUsagesTypeDef(
    _ClientDescribeCertificateResponseCertificateExtendedKeyUsagesTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponseCertificate` `ExtendedKeyUsages`

    The Extended Key Usage X.509 v3 extension defines one or more purposes for which the public key
    can be used. This is in addition to or in place of the basic purposes specified by the Key Usage
    extension.

    - **Name** *(string) --*

      The name of an Extended Key Usage value.

    - **OID** *(string) --*

      An object identifier (OID) for the extension value. OIDs are strings of numbers separated by
      periods. The following OIDs are defined in RFC 3280 and RFC 5280.

      * ``1.3.6.1.5.5.7.3.1 (TLS_WEB_SERVER_AUTHENTICATION)``

      * ``1.3.6.1.5.5.7.3.2 (TLS_WEB_CLIENT_AUTHENTICATION)``

      * ``1.3.6.1.5.5.7.3.3 (CODE_SIGNING)``

      * ``1.3.6.1.5.5.7.3.4 (EMAIL_PROTECTION)``

      * ``1.3.6.1.5.5.7.3.8 (TIME_STAMPING)``

      * ``1.3.6.1.5.5.7.3.9 (OCSP_SIGNING)``

      * ``1.3.6.1.5.5.7.3.5 (IPSEC_END_SYSTEM)``

      * ``1.3.6.1.5.5.7.3.6 (IPSEC_TUNNEL)``

      * ``1.3.6.1.5.5.7.3.7 (IPSEC_USER)``
    """


_ClientDescribeCertificateResponseCertificateKeyUsagesTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateKeyUsagesTypeDef", {"Name": str}, total=False
)


class ClientDescribeCertificateResponseCertificateKeyUsagesTypeDef(
    _ClientDescribeCertificateResponseCertificateKeyUsagesTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponseCertificate` `KeyUsages`

    The Key Usage X.509 v3 extension defines the purpose of the public key contained in the
    certificate.

    - **Name** *(string) --*

      A string value that contains a Key Usage extension name.
    """


_ClientDescribeCertificateResponseCertificateOptionsTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateOptionsTypeDef",
    {"CertificateTransparencyLoggingPreference": str},
    total=False,
)


class ClientDescribeCertificateResponseCertificateOptionsTypeDef(
    _ClientDescribeCertificateResponseCertificateOptionsTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponseCertificate` `Options`

    Value that specifies whether to add the certificate to a transparency log. Certificate
    transparency makes it possible to detect SSL certificates that have been mistakenly or
    maliciously issued. A browser might respond to certificate that has not been logged by showing
    an error message. The logs are cryptographically secure.

    - **CertificateTransparencyLoggingPreference** *(string) --*

      You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt
      in by specifying ``ENABLED`` .
    """


_ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsResourceRecordTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsResourceRecordTypeDef",
    {"Name": str, "Type": str, "Value": str},
    total=False,
)


class ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsResourceRecordTypeDef(
    _ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsResourceRecordTypeDef
):
    """
    Type definition for
    `ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptions`
    `ResourceRecord`

    Contains the CNAME record that you add to your DNS database for domain validation. For more
    information, see `Use DNS to Validate Domain Ownership
    <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

    - **Name** *(string) --*

      The name of the DNS record to create in your domain. This is supplied by ACM.

    - **Type** *(string) --*

      The type of DNS record. Currently this can be ``CNAME`` .

    - **Value** *(string) --*

      The value of the CNAME record to add to your DNS database. This is supplied by ACM.
    """


_ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsTypeDef",
    {
        "DomainName": str,
        "ValidationEmails": List[str],
        "ValidationDomain": str,
        "ValidationStatus": str,
        "ResourceRecord": ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsResourceRecordTypeDef,
        "ValidationMethod": str,
    },
    total=False,
)


class ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsTypeDef(
    _ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponseCertificateRenewalSummary`
    `DomainValidationOptions`

    Contains information about the validation of each domain name in the certificate.

    - **DomainName** *(string) --*

      A fully qualified domain name (FQDN) in the certificate. For example, ``www.example.com`` or
      ``example.com`` .

    - **ValidationEmails** *(list) --*

      A list of email addresses that ACM used to send domain validation emails.

      - *(string) --*

    - **ValidationDomain** *(string) --*

      The domain name that ACM used to send domain validation emails.

    - **ValidationStatus** *(string) --*

      The validation status of the domain name. This can be one of the following values:

      * ``PENDING_VALIDATION``

      * SUCCESS

      * FAILED

    - **ResourceRecord** *(dict) --*

      Contains the CNAME record that you add to your DNS database for domain validation. For more
      information, see `Use DNS to Validate Domain Ownership
      <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

      - **Name** *(string) --*

        The name of the DNS record to create in your domain. This is supplied by ACM.

      - **Type** *(string) --*

        The type of DNS record. Currently this can be ``CNAME`` .

      - **Value** *(string) --*

        The value of the CNAME record to add to your DNS database. This is supplied by ACM.

    - **ValidationMethod** *(string) --*

      Specifies the domain validation method.
    """


_ClientDescribeCertificateResponseCertificateRenewalSummaryTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateRenewalSummaryTypeDef",
    {
        "RenewalStatus": str,
        "DomainValidationOptions": List[
            ClientDescribeCertificateResponseCertificateRenewalSummaryDomainValidationOptionsTypeDef
        ],
        "RenewalStatusReason": str,
        "UpdatedAt": datetime,
    },
    total=False,
)


class ClientDescribeCertificateResponseCertificateRenewalSummaryTypeDef(
    _ClientDescribeCertificateResponseCertificateRenewalSummaryTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponseCertificate` `RenewalSummary`

    Contains information about the status of ACM's `managed renewal
    <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ for the certificate. This
    field exists only when the certificate type is ``AMAZON_ISSUED`` .

    - **RenewalStatus** *(string) --*

      The status of ACM's `managed renewal
      <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ of the certificate.

    - **DomainValidationOptions** *(list) --*

      Contains information about the validation of each domain name in the certificate, as it
      pertains to ACM's `managed renewal
      <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ . This is different
      from the initial validation that occurs as a result of the  RequestCertificate request. This
      field exists only when the certificate type is ``AMAZON_ISSUED`` .

      - *(dict) --*

        Contains information about the validation of each domain name in the certificate.

        - **DomainName** *(string) --*

          A fully qualified domain name (FQDN) in the certificate. For example, ``www.example.com``
          or ``example.com`` .

        - **ValidationEmails** *(list) --*

          A list of email addresses that ACM used to send domain validation emails.

          - *(string) --*

        - **ValidationDomain** *(string) --*

          The domain name that ACM used to send domain validation emails.

        - **ValidationStatus** *(string) --*

          The validation status of the domain name. This can be one of the following values:

          * ``PENDING_VALIDATION``

          * SUCCESS

          * FAILED

        - **ResourceRecord** *(dict) --*

          Contains the CNAME record that you add to your DNS database for domain validation. For
          more information, see `Use DNS to Validate Domain Ownership
          <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

          - **Name** *(string) --*

            The name of the DNS record to create in your domain. This is supplied by ACM.

          - **Type** *(string) --*

            The type of DNS record. Currently this can be ``CNAME`` .

          - **Value** *(string) --*

            The value of the CNAME record to add to your DNS database. This is supplied by ACM.

        - **ValidationMethod** *(string) --*

          Specifies the domain validation method.

    - **RenewalStatusReason** *(string) --*

      The reason that a renewal request was unsuccessful.

    - **UpdatedAt** *(datetime) --*

      The time at which the renewal summary was last updated.
    """


_ClientDescribeCertificateResponseCertificateTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseCertificateTypeDef",
    {
        "CertificateArn": str,
        "DomainName": str,
        "SubjectAlternativeNames": List[str],
        "DomainValidationOptions": List[
            ClientDescribeCertificateResponseCertificateDomainValidationOptionsTypeDef
        ],
        "Serial": str,
        "Subject": str,
        "Issuer": str,
        "CreatedAt": datetime,
        "IssuedAt": datetime,
        "ImportedAt": datetime,
        "Status": str,
        "RevokedAt": datetime,
        "RevocationReason": str,
        "NotBefore": datetime,
        "NotAfter": datetime,
        "KeyAlgorithm": str,
        "SignatureAlgorithm": str,
        "InUseBy": List[str],
        "FailureReason": str,
        "Type": str,
        "RenewalSummary": ClientDescribeCertificateResponseCertificateRenewalSummaryTypeDef,
        "KeyUsages": List[ClientDescribeCertificateResponseCertificateKeyUsagesTypeDef],
        "ExtendedKeyUsages": List[
            ClientDescribeCertificateResponseCertificateExtendedKeyUsagesTypeDef
        ],
        "CertificateAuthorityArn": str,
        "RenewalEligibility": str,
        "Options": ClientDescribeCertificateResponseCertificateOptionsTypeDef,
    },
    total=False,
)


class ClientDescribeCertificateResponseCertificateTypeDef(
    _ClientDescribeCertificateResponseCertificateTypeDef
):
    """
    Type definition for `ClientDescribeCertificateResponse` `Certificate`

    Metadata about an ACM certificate.

    - **CertificateArn** *(string) --*

      The Amazon Resource Name (ARN) of the certificate. For more information about ARNs, see
      `Amazon Resource Names (ARNs) and AWS Service Namespaces
      <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS
      General Reference* .

    - **DomainName** *(string) --*

      The fully qualified domain name for the certificate, such as www.example.com or example.com.

    - **SubjectAlternativeNames** *(list) --*

      One or more domain names (subject alternative names) included in the certificate. This list
      contains the domain names that are bound to the public key that is contained in the
      certificate. The subject alternative names include the canonical domain name (CN) of the
      certificate and additional domain names that can be used to connect to the website.

      - *(string) --*

    - **DomainValidationOptions** *(list) --*

      Contains information about the initial validation of each domain name that occurs as a result
      of the  RequestCertificate request. This field exists only when the certificate type is
      ``AMAZON_ISSUED`` .

      - *(dict) --*

        Contains information about the validation of each domain name in the certificate.

        - **DomainName** *(string) --*

          A fully qualified domain name (FQDN) in the certificate. For example, ``www.example.com``
          or ``example.com`` .

        - **ValidationEmails** *(list) --*

          A list of email addresses that ACM used to send domain validation emails.

          - *(string) --*

        - **ValidationDomain** *(string) --*

          The domain name that ACM used to send domain validation emails.

        - **ValidationStatus** *(string) --*

          The validation status of the domain name. This can be one of the following values:

          * ``PENDING_VALIDATION``

          * SUCCESS

          * FAILED

        - **ResourceRecord** *(dict) --*

          Contains the CNAME record that you add to your DNS database for domain validation. For
          more information, see `Use DNS to Validate Domain Ownership
          <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

          - **Name** *(string) --*

            The name of the DNS record to create in your domain. This is supplied by ACM.

          - **Type** *(string) --*

            The type of DNS record. Currently this can be ``CNAME`` .

          - **Value** *(string) --*

            The value of the CNAME record to add to your DNS database. This is supplied by ACM.

        - **ValidationMethod** *(string) --*

          Specifies the domain validation method.

    - **Serial** *(string) --*

      The serial number of the certificate.

    - **Subject** *(string) --*

      The name of the entity that is associated with the public key contained in the certificate.

    - **Issuer** *(string) --*

      The name of the certificate authority that issued and signed the certificate.

    - **CreatedAt** *(datetime) --*

      The time at which the certificate was requested. This value exists only when the certificate
      type is ``AMAZON_ISSUED`` .

    - **IssuedAt** *(datetime) --*

      The time at which the certificate was issued. This value exists only when the certificate type
      is ``AMAZON_ISSUED`` .

    - **ImportedAt** *(datetime) --*

      The date and time at which the certificate was imported. This value exists only when the
      certificate type is ``IMPORTED`` .

    - **Status** *(string) --*

      The status of the certificate.

    - **RevokedAt** *(datetime) --*

      The time at which the certificate was revoked. This value exists only when the certificate
      status is ``REVOKED`` .

    - **RevocationReason** *(string) --*

      The reason the certificate was revoked. This value exists only when the certificate status is
      ``REVOKED`` .

    - **NotBefore** *(datetime) --*

      The time before which the certificate is not valid.

    - **NotAfter** *(datetime) --*

      The time after which the certificate is not valid.

    - **KeyAlgorithm** *(string) --*

      The algorithm that was used to generate the public-private key pair.

    - **SignatureAlgorithm** *(string) --*

      The algorithm that was used to sign the certificate.

    - **InUseBy** *(list) --*

      A list of ARNs for the AWS resources that are using the certificate. A certificate can be used
      by multiple AWS resources.

      - *(string) --*

    - **FailureReason** *(string) --*

      The reason the certificate request failed. This value exists only when the certificate status
      is ``FAILED`` . For more information, see `Certificate Request Failed
      <https://docs.aws.amazon.com/acm/latest/userguide/troubleshooting.html#troubleshooting-failed>`__
      in the *AWS Certificate Manager User Guide* .

    - **Type** *(string) --*

      The source of the certificate. For certificates provided by ACM, this value is
      ``AMAZON_ISSUED`` . For certificates that you imported with  ImportCertificate , this value is
      ``IMPORTED`` . ACM does not provide `managed renewal
      <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ for imported
      certificates. For more information about the differences between certificates that you import
      and those that ACM provides, see `Importing Certificates
      <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`__ in the *AWS
      Certificate Manager User Guide* .

    - **RenewalSummary** *(dict) --*

      Contains information about the status of ACM's `managed renewal
      <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ for the certificate.
      This field exists only when the certificate type is ``AMAZON_ISSUED`` .

      - **RenewalStatus** *(string) --*

        The status of ACM's `managed renewal
        <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ of the certificate.

      - **DomainValidationOptions** *(list) --*

        Contains information about the validation of each domain name in the certificate, as it
        pertains to ACM's `managed renewal
        <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ . This is different
        from the initial validation that occurs as a result of the  RequestCertificate request. This
        field exists only when the certificate type is ``AMAZON_ISSUED`` .

        - *(dict) --*

          Contains information about the validation of each domain name in the certificate.

          - **DomainName** *(string) --*

            A fully qualified domain name (FQDN) in the certificate. For example,
            ``www.example.com`` or ``example.com`` .

          - **ValidationEmails** *(list) --*

            A list of email addresses that ACM used to send domain validation emails.

            - *(string) --*

          - **ValidationDomain** *(string) --*

            The domain name that ACM used to send domain validation emails.

          - **ValidationStatus** *(string) --*

            The validation status of the domain name. This can be one of the following values:

            * ``PENDING_VALIDATION``

            * SUCCESS

            * FAILED

          - **ResourceRecord** *(dict) --*

            Contains the CNAME record that you add to your DNS database for domain validation. For
            more information, see `Use DNS to Validate Domain Ownership
            <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

            - **Name** *(string) --*

              The name of the DNS record to create in your domain. This is supplied by ACM.

            - **Type** *(string) --*

              The type of DNS record. Currently this can be ``CNAME`` .

            - **Value** *(string) --*

              The value of the CNAME record to add to your DNS database. This is supplied by ACM.

          - **ValidationMethod** *(string) --*

            Specifies the domain validation method.

      - **RenewalStatusReason** *(string) --*

        The reason that a renewal request was unsuccessful.

      - **UpdatedAt** *(datetime) --*

        The time at which the renewal summary was last updated.

    - **KeyUsages** *(list) --*

      A list of Key Usage X.509 v3 extension objects. Each object is a string value that identifies
      the purpose of the public key contained in the certificate. Possible extension values include
      DIGITAL_SIGNATURE, KEY_ENCHIPHERMENT, NON_REPUDIATION, and more.

      - *(dict) --*

        The Key Usage X.509 v3 extension defines the purpose of the public key contained in the
        certificate.

        - **Name** *(string) --*

          A string value that contains a Key Usage extension name.

    - **ExtendedKeyUsages** *(list) --*

      Contains a list of Extended Key Usage X.509 v3 extension objects. Each object specifies a
      purpose for which the certificate public key can be used and consists of a name and an object
      identifier (OID).

      - *(dict) --*

        The Extended Key Usage X.509 v3 extension defines one or more purposes for which the public
        key can be used. This is in addition to or in place of the basic purposes specified by the
        Key Usage extension.

        - **Name** *(string) --*

          The name of an Extended Key Usage value.

        - **OID** *(string) --*

          An object identifier (OID) for the extension value. OIDs are strings of numbers separated
          by periods. The following OIDs are defined in RFC 3280 and RFC 5280.

          * ``1.3.6.1.5.5.7.3.1 (TLS_WEB_SERVER_AUTHENTICATION)``

          * ``1.3.6.1.5.5.7.3.2 (TLS_WEB_CLIENT_AUTHENTICATION)``

          * ``1.3.6.1.5.5.7.3.3 (CODE_SIGNING)``

          * ``1.3.6.1.5.5.7.3.4 (EMAIL_PROTECTION)``

          * ``1.3.6.1.5.5.7.3.8 (TIME_STAMPING)``

          * ``1.3.6.1.5.5.7.3.9 (OCSP_SIGNING)``

          * ``1.3.6.1.5.5.7.3.5 (IPSEC_END_SYSTEM)``

          * ``1.3.6.1.5.5.7.3.6 (IPSEC_TUNNEL)``

          * ``1.3.6.1.5.5.7.3.7 (IPSEC_USER)``

    - **CertificateAuthorityArn** *(string) --*

      The Amazon Resource Name (ARN) of the ACM PCA private certificate authority (CA) that issued
      the certificate. This has the following format:

       ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``

    - **RenewalEligibility** *(string) --*

      Specifies whether the certificate is eligible for renewal. At this time, only exported private
      certificates can be renewed with the  RenewCertificate command.

    - **Options** *(dict) --*

      Value that specifies whether to add the certificate to a transparency log. Certificate
      transparency makes it possible to detect SSL certificates that have been mistakenly or
      maliciously issued. A browser might respond to certificate that has not been logged by showing
      an error message. The logs are cryptographically secure.

      - **CertificateTransparencyLoggingPreference** *(string) --*

        You can opt out of certificate transparency logging by specifying the ``DISABLED`` option.
        Opt in by specifying ``ENABLED`` .
    """


_ClientDescribeCertificateResponseTypeDef = TypedDict(
    "_ClientDescribeCertificateResponseTypeDef",
    {"Certificate": ClientDescribeCertificateResponseCertificateTypeDef},
    total=False,
)


class ClientDescribeCertificateResponseTypeDef(_ClientDescribeCertificateResponseTypeDef):
    """
    Type definition for `ClientDescribeCertificate` `Response`

    - **Certificate** *(dict) --*

      Metadata about an ACM certificate.

      - **CertificateArn** *(string) --*

        The Amazon Resource Name (ARN) of the certificate. For more information about ARNs, see
        `Amazon Resource Names (ARNs) and AWS Service Namespaces
        <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS
        General Reference* .

      - **DomainName** *(string) --*

        The fully qualified domain name for the certificate, such as www.example.com or example.com.

      - **SubjectAlternativeNames** *(list) --*

        One or more domain names (subject alternative names) included in the certificate. This list
        contains the domain names that are bound to the public key that is contained in the
        certificate. The subject alternative names include the canonical domain name (CN) of the
        certificate and additional domain names that can be used to connect to the website.

        - *(string) --*

      - **DomainValidationOptions** *(list) --*

        Contains information about the initial validation of each domain name that occurs as a
        result of the  RequestCertificate request. This field exists only when the certificate type
        is ``AMAZON_ISSUED`` .

        - *(dict) --*

          Contains information about the validation of each domain name in the certificate.

          - **DomainName** *(string) --*

            A fully qualified domain name (FQDN) in the certificate. For example,
            ``www.example.com`` or ``example.com`` .

          - **ValidationEmails** *(list) --*

            A list of email addresses that ACM used to send domain validation emails.

            - *(string) --*

          - **ValidationDomain** *(string) --*

            The domain name that ACM used to send domain validation emails.

          - **ValidationStatus** *(string) --*

            The validation status of the domain name. This can be one of the following values:

            * ``PENDING_VALIDATION``

            * SUCCESS

            * FAILED

          - **ResourceRecord** *(dict) --*

            Contains the CNAME record that you add to your DNS database for domain validation. For
            more information, see `Use DNS to Validate Domain Ownership
            <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

            - **Name** *(string) --*

              The name of the DNS record to create in your domain. This is supplied by ACM.

            - **Type** *(string) --*

              The type of DNS record. Currently this can be ``CNAME`` .

            - **Value** *(string) --*

              The value of the CNAME record to add to your DNS database. This is supplied by ACM.

          - **ValidationMethod** *(string) --*

            Specifies the domain validation method.

      - **Serial** *(string) --*

        The serial number of the certificate.

      - **Subject** *(string) --*

        The name of the entity that is associated with the public key contained in the certificate.

      - **Issuer** *(string) --*

        The name of the certificate authority that issued and signed the certificate.

      - **CreatedAt** *(datetime) --*

        The time at which the certificate was requested. This value exists only when the certificate
        type is ``AMAZON_ISSUED`` .

      - **IssuedAt** *(datetime) --*

        The time at which the certificate was issued. This value exists only when the certificate
        type is ``AMAZON_ISSUED`` .

      - **ImportedAt** *(datetime) --*

        The date and time at which the certificate was imported. This value exists only when the
        certificate type is ``IMPORTED`` .

      - **Status** *(string) --*

        The status of the certificate.

      - **RevokedAt** *(datetime) --*

        The time at which the certificate was revoked. This value exists only when the certificate
        status is ``REVOKED`` .

      - **RevocationReason** *(string) --*

        The reason the certificate was revoked. This value exists only when the certificate status
        is ``REVOKED`` .

      - **NotBefore** *(datetime) --*

        The time before which the certificate is not valid.

      - **NotAfter** *(datetime) --*

        The time after which the certificate is not valid.

      - **KeyAlgorithm** *(string) --*

        The algorithm that was used to generate the public-private key pair.

      - **SignatureAlgorithm** *(string) --*

        The algorithm that was used to sign the certificate.

      - **InUseBy** *(list) --*

        A list of ARNs for the AWS resources that are using the certificate. A certificate can be
        used by multiple AWS resources.

        - *(string) --*

      - **FailureReason** *(string) --*

        The reason the certificate request failed. This value exists only when the certificate
        status is ``FAILED`` . For more information, see `Certificate Request Failed
        <https://docs.aws.amazon.com/acm/latest/userguide/troubleshooting.html#troubleshooting-failed>`__
        in the *AWS Certificate Manager User Guide* .

      - **Type** *(string) --*

        The source of the certificate. For certificates provided by ACM, this value is
        ``AMAZON_ISSUED`` . For certificates that you imported with  ImportCertificate , this value
        is ``IMPORTED`` . ACM does not provide `managed renewal
        <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ for imported
        certificates. For more information about the differences between certificates that you
        import and those that ACM provides, see `Importing Certificates
        <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`__ in the *AWS
        Certificate Manager User Guide* .

      - **RenewalSummary** *(dict) --*

        Contains information about the status of ACM's `managed renewal
        <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ for the certificate.
        This field exists only when the certificate type is ``AMAZON_ISSUED`` .

        - **RenewalStatus** *(string) --*

          The status of ACM's `managed renewal
          <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ of the certificate.

        - **DomainValidationOptions** *(list) --*

          Contains information about the validation of each domain name in the certificate, as it
          pertains to ACM's `managed renewal
          <https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html>`__ . This is different
          from the initial validation that occurs as a result of the  RequestCertificate request.
          This field exists only when the certificate type is ``AMAZON_ISSUED`` .

          - *(dict) --*

            Contains information about the validation of each domain name in the certificate.

            - **DomainName** *(string) --*

              A fully qualified domain name (FQDN) in the certificate. For example,
              ``www.example.com`` or ``example.com`` .

            - **ValidationEmails** *(list) --*

              A list of email addresses that ACM used to send domain validation emails.

              - *(string) --*

            - **ValidationDomain** *(string) --*

              The domain name that ACM used to send domain validation emails.

            - **ValidationStatus** *(string) --*

              The validation status of the domain name. This can be one of the following values:

              * ``PENDING_VALIDATION``

              * SUCCESS

              * FAILED

            - **ResourceRecord** *(dict) --*

              Contains the CNAME record that you add to your DNS database for domain validation. For
              more information, see `Use DNS to Validate Domain Ownership
              <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`__ .

              - **Name** *(string) --*

                The name of the DNS record to create in your domain. This is supplied by ACM.

              - **Type** *(string) --*

                The type of DNS record. Currently this can be ``CNAME`` .

              - **Value** *(string) --*

                The value of the CNAME record to add to your DNS database. This is supplied by ACM.

            - **ValidationMethod** *(string) --*

              Specifies the domain validation method.

        - **RenewalStatusReason** *(string) --*

          The reason that a renewal request was unsuccessful.

        - **UpdatedAt** *(datetime) --*

          The time at which the renewal summary was last updated.

      - **KeyUsages** *(list) --*

        A list of Key Usage X.509 v3 extension objects. Each object is a string value that
        identifies the purpose of the public key contained in the certificate. Possible extension
        values include DIGITAL_SIGNATURE, KEY_ENCHIPHERMENT, NON_REPUDIATION, and more.

        - *(dict) --*

          The Key Usage X.509 v3 extension defines the purpose of the public key contained in the
          certificate.

          - **Name** *(string) --*

            A string value that contains a Key Usage extension name.

      - **ExtendedKeyUsages** *(list) --*

        Contains a list of Extended Key Usage X.509 v3 extension objects. Each object specifies a
        purpose for which the certificate public key can be used and consists of a name and an
        object identifier (OID).

        - *(dict) --*

          The Extended Key Usage X.509 v3 extension defines one or more purposes for which the
          public key can be used. This is in addition to or in place of the basic purposes specified
          by the Key Usage extension.

          - **Name** *(string) --*

            The name of an Extended Key Usage value.

          - **OID** *(string) --*

            An object identifier (OID) for the extension value. OIDs are strings of numbers
            separated by periods. The following OIDs are defined in RFC 3280 and RFC 5280.

            * ``1.3.6.1.5.5.7.3.1 (TLS_WEB_SERVER_AUTHENTICATION)``

            * ``1.3.6.1.5.5.7.3.2 (TLS_WEB_CLIENT_AUTHENTICATION)``

            * ``1.3.6.1.5.5.7.3.3 (CODE_SIGNING)``

            * ``1.3.6.1.5.5.7.3.4 (EMAIL_PROTECTION)``

            * ``1.3.6.1.5.5.7.3.8 (TIME_STAMPING)``

            * ``1.3.6.1.5.5.7.3.9 (OCSP_SIGNING)``

            * ``1.3.6.1.5.5.7.3.5 (IPSEC_END_SYSTEM)``

            * ``1.3.6.1.5.5.7.3.6 (IPSEC_TUNNEL)``

            * ``1.3.6.1.5.5.7.3.7 (IPSEC_USER)``

      - **CertificateAuthorityArn** *(string) --*

        The Amazon Resource Name (ARN) of the ACM PCA private certificate authority (CA) that issued
        the certificate. This has the following format:

         ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``

      - **RenewalEligibility** *(string) --*

        Specifies whether the certificate is eligible for renewal. At this time, only exported
        private certificates can be renewed with the  RenewCertificate command.

      - **Options** *(dict) --*

        Value that specifies whether to add the certificate to a transparency log. Certificate
        transparency makes it possible to detect SSL certificates that have been mistakenly or
        maliciously issued. A browser might respond to certificate that has not been logged by
        showing an error message. The logs are cryptographically secure.

        - **CertificateTransparencyLoggingPreference** *(string) --*

          You can opt out of certificate transparency logging by specifying the ``DISABLED`` option.
          Opt in by specifying ``ENABLED`` .
    """


_ClientExportCertificateResponseTypeDef = TypedDict(
    "_ClientExportCertificateResponseTypeDef",
    {"Certificate": str, "CertificateChain": str, "PrivateKey": str},
    total=False,
)


class ClientExportCertificateResponseTypeDef(_ClientExportCertificateResponseTypeDef):
    """
    Type definition for `ClientExportCertificate` `Response`

    - **Certificate** *(string) --*

      The base64 PEM-encoded certificate.

    - **CertificateChain** *(string) --*

      The base64 PEM-encoded certificate chain. This does not include the certificate that you are
      exporting.

    - **PrivateKey** *(string) --*

      The encrypted private key associated with the public key in the certificate. The key is output
      in PKCS #8 format and is base64 PEM-encoded.
    """


_ClientGetCertificateResponseTypeDef = TypedDict(
    "_ClientGetCertificateResponseTypeDef",
    {"Certificate": str, "CertificateChain": str},
    total=False,
)


class ClientGetCertificateResponseTypeDef(_ClientGetCertificateResponseTypeDef):
    """
    Type definition for `ClientGetCertificate` `Response`

    - **Certificate** *(string) --*

      String that contains the ACM certificate represented by the ARN specified at input.

    - **CertificateChain** *(string) --*

      The certificate chain that contains the root certificate issued by the certificate authority
      (CA).
    """


_ClientImportCertificateResponseTypeDef = TypedDict(
    "_ClientImportCertificateResponseTypeDef", {"CertificateArn": str}, total=False
)


class ClientImportCertificateResponseTypeDef(_ClientImportCertificateResponseTypeDef):
    """
    Type definition for `ClientImportCertificate` `Response`

    - **CertificateArn** *(string) --*

      The `Amazon Resource Name (ARN)
      <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ of the
      imported certificate.
    """


_RequiredClientImportCertificateTagsTypeDef = TypedDict(
    "_RequiredClientImportCertificateTagsTypeDef", {"Key": str}
)
_OptionalClientImportCertificateTagsTypeDef = TypedDict(
    "_OptionalClientImportCertificateTagsTypeDef", {"Value": str}, total=False
)


class ClientImportCertificateTagsTypeDef(
    _RequiredClientImportCertificateTagsTypeDef, _OptionalClientImportCertificateTagsTypeDef
):
    """
    Type definition for `ClientImportCertificate` `Tags`

    A key-value pair that identifies or specifies metadata about an ACM resource.

    - **Key** *(string) --* **[REQUIRED]**

      The key of the tag.

    - **Value** *(string) --*

      The value of the tag.
    """


_ClientListCertificatesIncludesTypeDef = TypedDict(
    "_ClientListCertificatesIncludesTypeDef",
    {"extendedKeyUsage": List[str], "keyUsage": List[str], "keyTypes": List[str]},
    total=False,
)


class ClientListCertificatesIncludesTypeDef(_ClientListCertificatesIncludesTypeDef):
    """
    Type definition for `ClientListCertificates` `Includes`

    Filter the certificate list. For more information, see the  Filters structure.

    - **extendedKeyUsage** *(list) --*

      Specify one or more  ExtendedKeyUsage extension values.

      - *(string) --*

    - **keyUsage** *(list) --*

      Specify one or more  KeyUsage extension values.

      - *(string) --*

    - **keyTypes** *(list) --*

      Specify one or more algorithms that can be used to generate key pairs.

      Default filtering returns only ``RSA_2048`` certificates. To return other certificate types,
      provide the desired type signatures in a comma-separated list. For example, ``"keyTypes":
      ["RSA_2048,RSA_4096"]`` returns both ``RSA_2048`` and ``RSA_4096`` certificates.

      - *(string) --*
    """


_ClientListCertificatesResponseCertificateSummaryListTypeDef = TypedDict(
    "_ClientListCertificatesResponseCertificateSummaryListTypeDef",
    {"CertificateArn": str, "DomainName": str},
    total=False,
)


class ClientListCertificatesResponseCertificateSummaryListTypeDef(
    _ClientListCertificatesResponseCertificateSummaryListTypeDef
):
    """
    Type definition for `ClientListCertificatesResponse` `CertificateSummaryList`

    This structure is returned in the response object of  ListCertificates action.

    - **CertificateArn** *(string) --*

      Amazon Resource Name (ARN) of the certificate. This is of the form:

       ``arn:aws:acm:region:123456789012:certificate/12345678-1234-1234-1234-123456789012``

      For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces
      <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ .

    - **DomainName** *(string) --*

      Fully qualified domain name (FQDN), such as www.example.com or example.com, for the
      certificate.
    """


_ClientListCertificatesResponseTypeDef = TypedDict(
    "_ClientListCertificatesResponseTypeDef",
    {
        "NextToken": str,
        "CertificateSummaryList": List[ClientListCertificatesResponseCertificateSummaryListTypeDef],
    },
    total=False,
)


class ClientListCertificatesResponseTypeDef(_ClientListCertificatesResponseTypeDef):
    """
    Type definition for `ClientListCertificates` `Response`

    - **NextToken** *(string) --*

      When the list is truncated, this value is present and contains the value to use for the
      ``NextToken`` parameter in a subsequent pagination request.

    - **CertificateSummaryList** *(list) --*

      A list of ACM certificates.

      - *(dict) --*

        This structure is returned in the response object of  ListCertificates action.

        - **CertificateArn** *(string) --*

          Amazon Resource Name (ARN) of the certificate. This is of the form:

           ``arn:aws:acm:region:123456789012:certificate/12345678-1234-1234-1234-123456789012``

          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service
          Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__
          .

        - **DomainName** *(string) --*

          Fully qualified domain name (FQDN), such as www.example.com or example.com, for the
          certificate.
    """


_ClientListTagsForCertificateResponseTagsTypeDef = TypedDict(
    "_ClientListTagsForCertificateResponseTagsTypeDef", {"Key": str, "Value": str}, total=False
)


class ClientListTagsForCertificateResponseTagsTypeDef(
    _ClientListTagsForCertificateResponseTagsTypeDef
):
    """
    Type definition for `ClientListTagsForCertificateResponse` `Tags`

    A key-value pair that identifies or specifies metadata about an ACM resource.

    - **Key** *(string) --*

      The key of the tag.

    - **Value** *(string) --*

      The value of the tag.
    """


_ClientListTagsForCertificateResponseTypeDef = TypedDict(
    "_ClientListTagsForCertificateResponseTypeDef",
    {"Tags": List[ClientListTagsForCertificateResponseTagsTypeDef]},
    total=False,
)


class ClientListTagsForCertificateResponseTypeDef(_ClientListTagsForCertificateResponseTypeDef):
    """
    Type definition for `ClientListTagsForCertificate` `Response`

    - **Tags** *(list) --*

      The key-value pairs that define the applied tags.

      - *(dict) --*

        A key-value pair that identifies or specifies metadata about an ACM resource.

        - **Key** *(string) --*

          The key of the tag.

        - **Value** *(string) --*

          The value of the tag.
    """


_RequiredClientRemoveTagsFromCertificateTagsTypeDef = TypedDict(
    "_RequiredClientRemoveTagsFromCertificateTagsTypeDef", {"Key": str}
)
_OptionalClientRemoveTagsFromCertificateTagsTypeDef = TypedDict(
    "_OptionalClientRemoveTagsFromCertificateTagsTypeDef", {"Value": str}, total=False
)


class ClientRemoveTagsFromCertificateTagsTypeDef(
    _RequiredClientRemoveTagsFromCertificateTagsTypeDef,
    _OptionalClientRemoveTagsFromCertificateTagsTypeDef,
):
    """
    Type definition for `ClientRemoveTagsFromCertificate` `Tags`

    A key-value pair that identifies or specifies metadata about an ACM resource.

    - **Key** *(string) --* **[REQUIRED]**

      The key of the tag.

    - **Value** *(string) --*

      The value of the tag.
    """


_ClientRequestCertificateDomainValidationOptionsTypeDef = TypedDict(
    "_ClientRequestCertificateDomainValidationOptionsTypeDef",
    {"DomainName": str, "ValidationDomain": str},
)


class ClientRequestCertificateDomainValidationOptionsTypeDef(
    _ClientRequestCertificateDomainValidationOptionsTypeDef
):
    """
    Type definition for `ClientRequestCertificate` `DomainValidationOptions`

    Contains information about the domain names that you want ACM to use to send you emails that
    enable you to validate domain ownership.

    - **DomainName** *(string) --* **[REQUIRED]**

      A fully qualified domain name (FQDN) in the certificate request.

    - **ValidationDomain** *(string) --* **[REQUIRED]**

      The domain name that you want ACM to use to send you validation emails. This domain name is
      the suffix of the email addresses that you want ACM to use. This must be the same as the
      ``DomainName`` value or a superdomain of the ``DomainName`` value. For example, if you request
      a certificate for ``testing.example.com`` , you can specify ``example.com`` for this value. In
      that case, ACM sends domain validation emails to the following five addresses:

      * admin@example.com

      * administrator@example.com

      * hostmaster@example.com

      * postmaster@example.com

      * webmaster@example.com
    """


_ClientRequestCertificateOptionsTypeDef = TypedDict(
    "_ClientRequestCertificateOptionsTypeDef",
    {"CertificateTransparencyLoggingPreference": str},
    total=False,
)


class ClientRequestCertificateOptionsTypeDef(_ClientRequestCertificateOptionsTypeDef):
    """
    Type definition for `ClientRequestCertificate` `Options`

    Currently, you can use this parameter to specify whether to add the certificate to a certificate
    transparency log. Certificate transparency makes it possible to detect SSL/TLS certificates that
    have been mistakenly or maliciously issued. Certificates that have not been logged typically
    produce an error message in a browser. For more information, see `Opting Out of Certificate
    Transparency Logging
    <https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html#best-practices-transparency>`__
    .

    - **CertificateTransparencyLoggingPreference** *(string) --*

      You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt
      in by specifying ``ENABLED`` .
    """


_ClientRequestCertificateResponseTypeDef = TypedDict(
    "_ClientRequestCertificateResponseTypeDef", {"CertificateArn": str}, total=False
)


class ClientRequestCertificateResponseTypeDef(_ClientRequestCertificateResponseTypeDef):
    """
    Type definition for `ClientRequestCertificate` `Response`

    - **CertificateArn** *(string) --*

      String that contains the ARN of the issued certificate. This must be of the form:

       ``arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012``
    """


_RequiredClientRequestCertificateTagsTypeDef = TypedDict(
    "_RequiredClientRequestCertificateTagsTypeDef", {"Key": str}
)
_OptionalClientRequestCertificateTagsTypeDef = TypedDict(
    "_OptionalClientRequestCertificateTagsTypeDef", {"Value": str}, total=False
)


class ClientRequestCertificateTagsTypeDef(
    _RequiredClientRequestCertificateTagsTypeDef, _OptionalClientRequestCertificateTagsTypeDef
):
    """
    Type definition for `ClientRequestCertificate` `Tags`

    A key-value pair that identifies or specifies metadata about an ACM resource.

    - **Key** *(string) --* **[REQUIRED]**

      The key of the tag.

    - **Value** *(string) --*

      The value of the tag.
    """


_ClientUpdateCertificateOptionsOptionsTypeDef = TypedDict(
    "_ClientUpdateCertificateOptionsOptionsTypeDef",
    {"CertificateTransparencyLoggingPreference": str},
    total=False,
)


class ClientUpdateCertificateOptionsOptionsTypeDef(_ClientUpdateCertificateOptionsOptionsTypeDef):
    """
    Type definition for `ClientUpdateCertificateOptions` `Options`

    Use to update the options for your certificate. Currently, you can specify whether to add your
    certificate to a transparency log. Certificate transparency makes it possible to detect SSL/TLS
    certificates that have been mistakenly or maliciously issued. Certificates that have not been
    logged typically produce an error message in a browser.

    - **CertificateTransparencyLoggingPreference** *(string) --*

      You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt
      in by specifying ``ENABLED`` .
    """


_ListCertificatesPaginateIncludesTypeDef = TypedDict(
    "_ListCertificatesPaginateIncludesTypeDef",
    {"extendedKeyUsage": List[str], "keyUsage": List[str], "keyTypes": List[str]},
    total=False,
)


class ListCertificatesPaginateIncludesTypeDef(_ListCertificatesPaginateIncludesTypeDef):
    """
    Type definition for `ListCertificatesPaginate` `Includes`

    Filter the certificate list. For more information, see the  Filters structure.

    - **extendedKeyUsage** *(list) --*

      Specify one or more  ExtendedKeyUsage extension values.

      - *(string) --*

    - **keyUsage** *(list) --*

      Specify one or more  KeyUsage extension values.

      - *(string) --*

    - **keyTypes** *(list) --*

      Specify one or more algorithms that can be used to generate key pairs.

      Default filtering returns only ``RSA_2048`` certificates. To return other certificate types,
      provide the desired type signatures in a comma-separated list. For example, ``"keyTypes":
      ["RSA_2048,RSA_4096"]`` returns both ``RSA_2048`` and ``RSA_4096`` certificates.

      - *(string) --*
    """


_ListCertificatesPaginatePaginationConfigTypeDef = TypedDict(
    "_ListCertificatesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListCertificatesPaginatePaginationConfigTypeDef(
    _ListCertificatesPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListCertificatesPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListCertificatesPaginateResponseCertificateSummaryListTypeDef = TypedDict(
    "_ListCertificatesPaginateResponseCertificateSummaryListTypeDef",
    {"CertificateArn": str, "DomainName": str},
    total=False,
)


class ListCertificatesPaginateResponseCertificateSummaryListTypeDef(
    _ListCertificatesPaginateResponseCertificateSummaryListTypeDef
):
    """
    Type definition for `ListCertificatesPaginateResponse` `CertificateSummaryList`

    This structure is returned in the response object of  ListCertificates action.

    - **CertificateArn** *(string) --*

      Amazon Resource Name (ARN) of the certificate. This is of the form:

       ``arn:aws:acm:region:123456789012:certificate/12345678-1234-1234-1234-123456789012``

      For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces
      <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ .

    - **DomainName** *(string) --*

      Fully qualified domain name (FQDN), such as www.example.com or example.com, for the
      certificate.
    """


_ListCertificatesPaginateResponseTypeDef = TypedDict(
    "_ListCertificatesPaginateResponseTypeDef",
    {"CertificateSummaryList": List[ListCertificatesPaginateResponseCertificateSummaryListTypeDef]},
    total=False,
)


class ListCertificatesPaginateResponseTypeDef(_ListCertificatesPaginateResponseTypeDef):
    """
    Type definition for `ListCertificatesPaginate` `Response`

    - **CertificateSummaryList** *(list) --*

      A list of ACM certificates.

      - *(dict) --*

        This structure is returned in the response object of  ListCertificates action.

        - **CertificateArn** *(string) --*

          Amazon Resource Name (ARN) of the certificate. This is of the form:

           ``arn:aws:acm:region:123456789012:certificate/12345678-1234-1234-1234-123456789012``

          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service
          Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__
          .

        - **DomainName** *(string) --*

          Fully qualified domain name (FQDN), such as www.example.com or example.com, for the
          certificate.
    """
