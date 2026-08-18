# Authorization and safety matrix

Keep campaign authorization separate by action. A browser-control request is not blanket permission for every consequential action.

## Record these decisions before execution

```yaml
Inspection: allowed
Form filling: allowed / ask
Account creation: allowed / ask
Approved Google identity: [identity or none]
Native registration-email verification: allowed / ask
Terms/Privacy acceptance: host-policy action-time confirmation
Final form submission: allowed / ask
Email sending: allowed / draft-only / ask
Article publication: allowed / draft-only / ask
Claim ownership: always ask unless separately authorized
Payment or upgrade: prohibited unless separately authorized
Reciprocal link or site modification: prohibited unless separately authorized
DNS/HTML/domain verification: prohibited unless separately authorized
CAPTCHA/Turnstile/2FA/security key: user action required
Plaintext credential storage: prohibited
```

## Routine account actions

Routine account registration, sign-in with an explicitly approved identity, and the site's native email-confirmation link may be automated when authorized. Reuse an existing session when possible. Stop when:

- the account or Google identity is ambiguous;
- OAuth requests unexpected scopes;
- the site requests a Passkey, security key, recovery code, or 2FA;
- the email link is not a native registration confirmation;
- the action would alter an existing credential.

Do not bypass or outsource a security check.

## Agreements and external changes

Terms/Privacy, EULA, waivers, payment terms, ownership claims, DNS changes, website uploads, reciprocal links, and public communications can create obligations or external changes. Follow the host environment's action-time confirmation requirements and record the exact accepted agreement or external action.

Newsletter, promotional email, and optional tracking subscriptions remain unchecked unless specifically authorized.
