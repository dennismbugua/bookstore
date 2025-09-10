# How to Get Your PayPal Sandbox Business Email

## Step 1: Access PayPal Developer Dashboard
1. Go to: https://developer.paypal.com/
2. Log in with your PayPal account

## Step 2: Find Your App
1. Go to "My Apps & Credentials"
2. Make sure you're in "Sandbox" mode (toggle at the top)
3. Find your app with Client ID: `AS6xp1f7LseLOpGg6bvK97dDkOaXM5dVp2ulBaNuQuEH1BC-ThPZYEZY0eYR7sWEjxcXAs-n4591LY6D`

## Step 3: Get Business Account Email
1. Click on your app name
2. Scroll down to find the "Sandbox Accounts" section
3. Look for the Business account (not Personal)
4. Copy the email address (it will look like: `sb-xxxxx@business.example.com`)

## Step 4: Update Django Settings
1. Replace `sb-43egm518143@business.example.com` in your settings.py with the actual email
2. Update both `PAYPAL_RECEIVER_EMAIL` and `PAYPAL_BUSINESS_EMAIL`

## Alternative: Create New Sandbox Account
If you don't see a business account:
1. In the Developer Dashboard, go to "Sandbox" > "Accounts"
2. Click "Create Account"
3. Select "Business" account type
4. Fill in the details and note the email address
5. Link this account to your app

## Test Email for Immediate Testing
If you want to test immediately, you can try using:
- `sb-dennis@business.example.com` (but this might not work)
- Better to get your actual sandbox business email from the dashboard

## Debugging
After updating the email, check the Django console output when you click "Pay with PayPal" - it will print all the PayPal form data being sent.
