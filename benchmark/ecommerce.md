# E-commerce Project - User Stories

**Project:** E-commerce System  
**Domain:** Online Shopping  
**Total User Stories:** 26  
**Total Acceptance Criteria:** 78  

---

## ECO-001: Browse Products by Category

**User Story:** As a customer, I want to browse products by category so that I can find items I'm interested in.

**Acceptance Criteria:**
1. Category list is displayed on homepage
2. Clicking category shows relevant products
3. Products show name, price, and image
4. Pagination works for large product lists
5. Search within category is available

---

## ECO-002: Search for Products

**User Story:** As a customer, I want to search for products so that I can quickly find specific items.

**Acceptance Criteria:**
1. Search bar is prominently displayed
2. Search results are relevant to keywords
3. Search supports partial matches
4. Empty search shows no results message
5. Search is case insensitive

---

## ECO-003: Add Products to Shopping Cart

**User Story:** As a customer, I want to add products to a shopping cart so that I can purchase multiple items.

**Acceptance Criteria:**
1. Add to cart button is visible on product page
2. Cart displays added items with quantities
3. Customer can update item quantities
4. Customer can remove items from cart
5. Cart total updates automatically

---

## ECO-004: View Shopping Cart

**User Story:** As a customer, I want to view my shopping cart so that I can review items before checkout.

**Acceptance Criteria:**
1. Cart shows all items with details
2. Cart shows subtotal and total
3. Cart shows shipping costs
4. Cart is persistent across sessions
5. Cart shows availability of items

---

## ECO-005: Checkout and Place Order

**User Story:** As a customer, I want to checkout and place an order so that I can purchase products.

**Acceptance Criteria:**
1. Checkout process has steps (shipping, payment, review)
2. Customer can enter shipping address
3. Customer can select payment method
4. Order summary is displayed before submission
5. Order confirmation is sent via email

---

## ECO-006: Save Products to Wishlist

**User Story:** As a customer, I want to save products to a wishlist so that I can purchase them later.

**Acceptance Criteria:**
1. Wishlist button is on product page
2. Wishlist items are saved to account
3. Customer can view wishlist
4. Customer can move items to cart
5. Customer can remove items from wishlist

---

## ECO-007: Apply Discount Codes

**User Story:** As a customer, I want to apply discount codes so that I can get discounts on my purchases.

**Acceptance Criteria:**
1. Discount code field is available at checkout
2. Valid codes are applied to order total
3. Invalid codes show error message
4. Discount amount is shown clearly
5. Expired codes are not accepted

---

## ECO-008: View Product Details

**User Story:** As a customer, I want to view product details so that I can make informed purchasing decisions.

**Acceptance Criteria:**
1. Product page shows detailed description
2. Product page shows price and availability
3. Product page shows specifications
4. Product page shows customer reviews
5. Product page shows related products

---

## ECO-009: Write Product Reviews

**User Story:** As a customer, I want to write product reviews so that I can share my experience.

**Acceptance Criteria:**
1. Review form is available on product page
2. Customer can rate products (1-5 stars)
3. Customer can write text review
4. Reviews are displayed publicly
5. Customers can edit/delete own reviews

---

## ECO-010: Track Orders

**User Story:** As a customer, I want to track my orders so that I can monitor delivery status.

**Acceptance Criteria:**
1. Order list shows all customer orders
2. Each order shows current status
3. Tracking number is displayed when shipped
4. Customer can view order details
5. Order status updates are visible

---

## ECO-011: Cancel Orders

**User Story:** As a customer, I want to cancel an order so that I can stop unwanted purchases.

**Acceptance Criteria:**
1. Cancel button is available on order page
2. Only cancellable orders have cancel option
3. Customer receives cancellation confirmation
4. Refund is processed if payment was made
5. Cancelled orders are removed from active orders

---

## ECO-012: Manage Account Profile

**User Story:** As a customer, I want to manage my account profile so that I can update my information.

**Acceptance Criteria:**
1. Customer can update personal information
2. Customer can change password
3. Customer can update email address
4. Customer can view order history
5. Profile changes are saved permanently

---

## ECO-013: Manage Addresses

**User Story:** As a customer, I want to manage my addresses so that I can use them for shipping.

**Acceptance Criteria:**
1. Customer can add multiple shipping addresses
2. Customer can set a default address
3. Customer can edit existing addresses
4. Customer can delete addresses
5. Addresses are validated for correctness

---

## ECO-014: Save Payment Methods

**User Story:** As a customer, I want to save payment methods so that I can checkout faster.

**Acceptance Criteria:**
1. Customer can add credit/debit cards
2. Customer can set default payment method
3. Customer can remove payment methods
4. Payment information is secure
5. Payment methods are encrypted

---

## ECO-015: Receive Notifications

**User Story:** As a customer, I want to receive notifications about orders so that I stay informed.

**Acceptance Criteria:**
1. Email notifications are sent for order confirmation
2. Email notifications are sent for shipping updates
3. Email notifications are sent for order delivery
4. SMS notifications for order status changes
5. Push notifications for mobile app

---

## ECO-016: Compare Products

**User Story:** As a customer, I want to compare products so that I can choose the best option.

**Acceptance Criteria:**
1. Compare button is available on product page
2. Compare list can hold multiple products
3. Comparison shows key features side-by-side
4. Comparison shows price differences
5. Customer can remove products from comparison

---

## ECO-017: Filter Products by Price

**User Story:** As a customer, I want to filter products by price so that I can find items in my budget.

**Acceptance Criteria:**
1. Price filter is available in search results
2. Customer can set minimum and maximum price
3. Price filter updates results immediately
4. Price filter works with other filters
5. Invalid price range shows error

---

## ECO-018: Sort Products

**User Story:** As a customer, I want to sort products by relevance so that I can find the best matches.

**Acceptance Criteria:**
1. Sort options include relevance, price, rating
2. Sort by price (low to high) works
3. Sort by price (high to low) works
4. Sort by rating works
5. Sort by newest works

---

## ECO-019: View Product Availability

**User Story:** As a customer, I want to see product availability so that I know if items are in stock.

**Acceptance Criteria:**
1. Stock status is shown on product page
2. Stock status is shown in search results
3. Out of stock items are marked clearly
4. Customer can be notified when out of stock items become available
5. Quantity limits are shown when applicable

---

## ECO-020: View Recommended Products

**User Story:** As a customer, I want to view recommended products so that I can discover new items.

**Acceptance Criteria:**
1. Recommended products are shown on product page
2. Recommendations are personalized
3. Recommendations based on browsing history
4. Recommendations based on purchase history
5. Customer can dismiss recommendations

---

## ECO-021: Guest Checkout

**User Story:** As a customer, I want to checkout as guest so that I don't have to create an account.

**Acceptance Criteria:**
1. Guest checkout option is available
2. Guest can enter shipping information
3. Guest can enter payment information
4. Guest receives order confirmation
5. Guest can optionally create account after checkout

---

## ECO-022: Return Products

**User Story:** As a customer, I want to return products so that I can get refunds for unsatisfactory items.

**Acceptance Criteria:**
1. Return request can be submitted from order page
2. Return reason is required
3. Return status can be tracked
4. Refund is processed for returned items
5. Return window is enforced

---

## ECO-023: Share Products on Social Media

**User Story:** As a customer, I want to share products on social media so that I can recommend to friends.

**Acceptance Criteria:**
1. Share buttons are on product page
2. Share to Facebook works
3. Share to Twitter works
4. Share via email works
5. Share link contains product information

---

## ECO-024: View Product Ratings

**User Story:** As a customer, I want to see product ratings so that I can judge quality.

**Acceptance Criteria:**
1. Average rating is displayed on product page
2. Rating distribution is shown
3. Individual reviews show user ratings
4. Most helpful reviews are highlighted
5. Rating filters are available

---

## ECO-025: View Product Images

**User Story:** As a customer, I want to view product images so that I can see the product clearly.

**Acceptance Criteria:**
1. Multiple product images are displayed
2. Image zoom is available
3. 360-degree view is available
4. Thumbnail navigation works
5. Images load quickly and show alt text

---

## ECO-026: Export Order History

**User Story:** As a customer, I want to export my order history so that I can keep records.

**Acceptance Criteria:**
1. Order history can be exported to CSV
2. Order history can be exported to PDF
3. Export includes all order details
4. Export includes dates and amounts
5. Export is downloadable

---

**Summary:**
- **Total Stories:** 26
- **Total Acceptance Criteria:** 130 (5 per story)
- **Domain:** E-commerce
