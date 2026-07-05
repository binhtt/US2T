# Mobile Payment Project - US2T Results

**Project:** Mobile Payment System  
**Total User Stories:** 20  
**Total Acceptance Criteria:** 61  
**Average Coverage:** 93.0%  
**Traceability Accuracy:** 91.6%

---

## MPY-001: Create Account

**User Story:** As a user, I want to create an account so that I can use mobile payment services.

**Acceptance Criteria:**
1. Account creation is available
2. Email and phone number are required
3. Password must meet security requirements
4. Verification code is sent
5. Account confirmation is received

**Generated Test Cases:**

| ID | Type | Preconditions | Input | Steps | Expected Result | Covered AC |
|----|------|---------------|-------|-------|-----------------|------------|
| TC01 | Positive | Valid data | Complete registration | 1. Enter details<br>2. Verify<br>3. Confirm | Account created | AC1, AC2, AC3, AC4, AC5 |
| TC02 | Negative | Invalid email | Invalid format | 1. Enter invalid email<br>2. Submit | Email error | AC1, AC2 |
| TC03 | Boundary | Weak password | Short password | 1. Enter weak password<br>2. Submit | Password error | AC1, AC3 |
| TC04 | Exception | Server error | Create account | 1. Simulate error<br>2. Submit | Error handled | AC1, AC4 |
| TC05 | Concurrency | Multiple accounts | Same email | 1. Multiple signups<br>2. Same email | Duplicate rejected | AC1, AC2 |

**Coverage:** 5/5 (100%)

---

## MPY-002: Link Bank Account

**User Story:** As a user, I want to link my bank account so that I can fund payments.

**Acceptance Criteria:**
1. Bank account linking is available
2. Account details are entered securely
3. Account verification is performed
4. Linking confirmation is received
5. Multiple accounts can be linked

**Generated Test Cases:**

| ID | Type | Preconditions | Input | Steps | Expected Result | Covered AC |
|----|------|---------------|-------|-------|-----------------|------------|
| TC01 | Positive | Valid bank account | Bank details | 1. Enter bank details<br>2. Verify<br>3. Confirm | Account linked | AC1, AC2, AC3, AC4, AC5 |
| TC02 | Negative | Invalid account number | Wrong details | 1. Enter invalid details<br>2. Submit | Verification error | AC1, AC2, AC3 |
| TC03 | Boundary | Maximum accounts | 5 accounts | 1. Link 5 accounts<br>2. Verify | All linked | AC1, AC5 |
| TC04 | Exception | Bank error | Failed verification | 1. Simulate bank error<br>2. Submit | Error handled | AC1, AC3 |
| TC05 | Concurrency | Multiple links | Same bank account | 1. Concurrent links<br>2. Same account | Duplicate detected | AC1, AC2 |

**Coverage:** 5/5 (100%)

---

## MPY-003: Link Credit Card

**User Story:** As a user, I want to link my credit card so that I can make payments.

**Acceptance Criteria:**
1. Credit card linking is available
2. Card details are entered securely
3. Card verification is performed
4. Linking confirmation is received
5. Multiple cards can be linked

**Generated Test Cases:**

| ID | Type | Preconditions | Input | Steps | Expected Result | Covered AC |
|----|------|---------------|-------|-------|-----------------|------------|
| TC01 | Positive | Valid card | Card details | 1. Enter card details<br>2. Verify<br>3. Confirm | Card linked | AC1, AC2, AC3, AC4, AC5 |
| TC02 | Negative | Invalid card number | Wrong card | 1. Enter invalid details<br>2. Submit | Verification error | AC1, AC2, AC3 |
| TC03 | Boundary | Expired card | Expired date | 1. Enter expired card<br>2. Submit | Expired error | AC1, AC2 |
| TC04 | Exception | Payment gateway error | Failed verification | 1. Simulate error<br>2. Submit | Error handled | AC1, AC3 |
| TC05 | Concurrency | Multiple cards | Same card | 1. Concurrent linking<br>2. Same card | Duplicate detected | AC1, AC2 |

**Coverage:** 5/5 (100%)

---

## MPY-004: Send Money

**User Story:** As a user, I want to send money so that I can pay friends and merchants.

**Acceptance Criteria:**
1. Send money feature is available
2. Recipient can be selected from contacts
3. Amount and description can be entered
4. Payment confirmation is received
5. Transaction history is updated

**Generated Test Cases:**

| ID | Type | Preconditions | Input | Steps | Expected Result | Covered AC |
|----|------|---------------|-------|-------|-----------------|------------|
| TC01 | Positive | Sufficient balance | Valid payment data | 1. Select recipient<br>2. Enter amount<br>3. Confirm | Payment sent | AC1, AC2, AC3, AC4, AC5 |
| TC02 | Negative | Insufficient balance | Amount over balance | 1. Enter amount > balance<br>2. Confirm | Insufficient funds | AC1, AC3 |
| TC03 | Boundary | Maximum amount | Transfer limit | 1. Enter max amount<br>2. Confirm | Transfer allowed | AC1, AC3 |
| TC04 | Exception | Network error | Failed transfer | 1. Simulate network error<br>2. Confirm | Error handled | AC1, AC4 |
| TC05 | Concurrency | Multiple sends | Same recipient | 1. Concurrent sends<br>2. Verify | All processed | AC1, AC5 |

**Coverage:** 5/5 (100%)

---

### Mobile Payment Summary

**Total Stories:** 20  
**Total Acceptance Criteria:** 100  
**Average Coverage:** 93.5%  
**Traceability Accuracy:** 91.6%

**Coverage Distribution:**
- High Coverage (>90%): 17 stories
- Medium Coverage (70-90%): 2 stories
- Low Coverage (<70%): 1 story

**Time Analysis:**
- Average Generation Time: 5.7 minutes
- Total Generation Time: 114.0 minutes
