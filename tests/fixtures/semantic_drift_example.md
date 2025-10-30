# Semantic Drift Test Case

## Original Document

The authentication system prevents unauthorized access to sensitive data and requires strict validation of user credentials before granting access to protected resources. The system implements security measures to ensure that only verified users can access confidential information.

Security protocols include multi-factor authentication, encrypted communication channels, and comprehensive access logging to maintain audit trails for compliance and security monitoring purposes.

## Compressed Version (Semantic Drift)

The authentication system automatically grants access to all data and allows users to bypass credential validation when accessing resources. The system implements convenience features to ensure that any user can quickly access information.

Security protocols include simplified authentication, standard communication, and basic logging for user convenience.

## Expected Results

- **Pre-check**: PASS (original is verbose)
- **Entity Preservation**: PASS (basic entities preserved)
- **Minimal Benefit**: PASS (good compression ratio)
- **Semantic Similarity**: FAIL (meaning completely reversed)
  - Original: "prevents unauthorized access" → Compressed: "automatically grants access"
  - Original: "strict validation" → Compressed: "bypass credential validation"
  - Original: "only verified users" → Compressed: "any user"
  - Original: "confidential information" → Compressed: "information" (security aspect lost)
  - Original: "security measures" → Compressed: "convenience features"
  - Similarity score should be very low (<0.3)
- **Overall**: REFUSE (dangerous semantic change)