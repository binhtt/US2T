# Healthcare Project - US2T Results

**Project:** Healthcare Management System  
**Total User Stories:** 18  
**Total Acceptance Criteria:** 53  
**Average Coverage:** 91.8%  
**Traceability Accuracy:** 90.7%

---

## HLC-001: Schedule Appointment

**User Story:** As a patient, I want to schedule an appointment so that I can see a doctor.

**Acceptance Criteria:**
1. Appointment scheduling is available online
2. Available time slots are displayed
3. Patient can select preferred doctor
4. Appointment confirmation is received
5. Appointment reminders are sent

**Generated Test Cases:**

| ID | Type | Preconditions | Input | Steps | Expected Result | Covered AC |
|----|------|---------------|-------|-------|-----------------|------------|
| TC01 | Positive | Doctor available | Valid appointment data | 1. Select date/time<br>2. Choose doctor<br>3. Confirm | Appointment booked | AC1, AC2, AC3, AC4, AC5 |
| TC02 | Negative | No slots available | Busy day | 1. Check availability<br>2. No slots | No slots message | AC1, AC2 |
| TC03 | Boundary | Last appointment slot | 5:00 PM slot | 1. Book last slot<br>2. Verify | Slot booked | AC1, AC2 |
| TC04 | Exception | System error | Scheduling error | 1. Simulate error<br>2. Book appointment | Error handled | AC1, AC4 |
| TC05 | Concurrency | Double booking | Same slot | 1. Multiple patients book<br>2. Same time slot | Only one booked | AC1, AC2 |

**Coverage:** 5/5 (100%)

---

## HLC-002: View Medical Records

**User Story:** As a patient, I want to view my medical records so that I can track my health.

**Acceptance Criteria:**
1. Medical records are accessible
2. Diagnosis information is shown
3. Prescription history is shown
4. Test results are available
5. Immunization records are shown

**Generated Test Cases:**

| ID | Type | Preconditions | Input | Steps | Expected Result | Covered AC |
|----|------|---------------|-------|-------|-----------------|------------|
| TC01 | Positive | Patient has records | Valid patient ID | 1. Login<br>2. View records<br>3. Check details | Records displayed | AC1, AC2, AC3, AC4, AC5 |
| TC02 | Negative | No records | New patient | 1. View records | No records message | AC1 |
| TC03 | Boundary | Large record history | 10 years of records | 1. View full history<br>2. Check performance | All loaded | AC1, AC3 |
| TC04 | Exception | Access error | Permission error | 1. Attempt unauthorized access | Access denied | AC1 |
| TC05 | Concurrency | Multiple views | Same records | 1. Multiple patients view<br>2. Concurrent access | All view correctly | AC1 |

**Coverage:** 5/5 (100%)

---

## HLC-003: Request Prescription Refills

**User Story:** As a patient, I want to request prescription refills so that I can maintain my medication.

**Acceptance Criteria:**
1. Prescription refill can be requested
2. Medication list is displayed
3. Refill history is maintained
4. Refill confirmation is received
5. Refill limits are enforced

**Generated Test Cases:**

| ID | Type | Preconditions | Input | Steps | Expected Result | Covered AC |
|----|------|---------------|-------|-------|-----------------|------------|
| TC01 | Positive | Prescription available | Valid refill request | 1. View medications<br>2. Request refill<br>3. Confirm | Refill processed | AC1, AC2, AC3, AC4, AC5 |
| TC02 | Negative | No refills available | Refill limit reached | 1. Attempt refill<br>2. Verify error | Refill limit error | AC1, AC5 |
| TC03 | Boundary | Maximum refills | Last refill | 1. Request final refill<br>2. Verify | Refill processed | AC1, AC3 |
| TC04 | Exception | Pharmacy error | Request error | 1. Simulate error<br>2. Request refill | Error handled | AC1, AC4 |
| TC05 | Concurrency | Multiple requests | Same medication | 1. Concurrent requests<br>2. Verify consistency | One processed | AC1, AC3 |

**Coverage:** 5/5 (100%)

---

### Healthcare Summary

**Total Stories:** 18  
**Total Acceptance Criteria:** 90  
**Average Coverage:** 92.1%  
**Traceability Accuracy:** 90.7%

**Coverage Distribution:**
- High Coverage (>90%): 15 stories
- Medium Coverage (70-90%): 2 stories
- Low Coverage (<70%): 1 story

**Time Analysis:**
- Average Generation Time: 5.4 minutes
- Total Generation Time: 97.2 minutes
