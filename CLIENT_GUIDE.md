# AI Receptionist for Your Roofing Company
## Simple Guide for Business Owners

---

## **What This System Does for You**

Your new AI Receptionist handles calls and texts 24/7, so you never miss a lead:

✅ **Missed Calls** → Automatically texts back: *"Sorry I missed you! I'm on a roof right now. How can I help you?"*

✅ **Text Messages** → AI chat named "Sarah" responds instantly, asks for their name, issue, and address

✅ **Live Monitoring** → Every customer text is forwarded to YOUR phone so you see all conversations

✅ **Lead Tracking** → All conversations saved to a spreadsheet (leads.csv)

✅ **Call Forwarding** → Calls ring your personal phone first (20 seconds), then auto-text if missed

---

## **What You Need to Provide**

### **1. Twilio Phone Number (Your Business Line)**
- This is the number customers call/text
- Cost: ~$1-2/month + usage
- Sign up: [twilio.com/console](https://www.twilio.com/console)

### **2. Your Personal Cell Phone**
- Where calls get forwarded
- Where you receive monitoring texts
- **Example:** +1 (704) 791-7540

### **3. Google Gemini API Key (FREE)**
- Powers the AI chat
- Get it: [ai.google.dev](https://ai.google.dev)
- Click "Get API Key" → Copy it

---

## **Setup Checklist (One-Time, 15 Minutes)**

### **Step 1: Twilio Account Setup**
1. Go to [twilio.com](https://www.twilio.com) → Sign up (trial is free)
2. Buy a phone number → Choose your area code → $1-2/month
3. Add payment method (required even for trial)
4. Verify your personal cell phone:
   - Console → **Verified Caller IDs** → Add your number

### **Step 2: Get Your Gemini API Key**
1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click **Create API Key** → Copy it
3. Save it somewhere safe

### **Step 3: Deploy Your Bot (We Handle This)**
We'll set this up for you on Render.com (FREE hosting):
- You'll get a permanent link like: `https://yourcompany-bot.onrender.com`
- No technical work needed from you

### **Step 4: Connect Twilio to Your Bot**
Go to Twilio Console → Phone Numbers → Your Number:

**For Voice Calls:**
- A Call Comes In: **Webhook**
- URL: `https://yourcompany-bot.onrender.com/voice`
- Method: **POST**

**For Text Messages:**
- A Message Comes In: **Webhook**
- URL: `https://yourcompany-bot.onrender.com/sms`
- Method: **POST**

Click **Save**

---

## **How to Use & Monitor**

### **Daily Operations (Zero Work Required)**
The system runs automatically. You just:
1. Answer your phone when it rings (forwarded calls)
2. Check texts on your phone (monitoring messages)
3. Review leads weekly in the CSV file

### **Monitoring Messages (What You'll See)**
When a customer texts, you get BOTH messages:
```
Customer (555-1234): "I need my roof fixed"
↓
Bot Reply: "Hi! I'm Sarah. Can I get your name and address?"
↓
Your Phone Gets: "[MONITOR] Customer (+15551234): I need my roof fixed | Bot: Hi! I'm Sarah..."
```

### **Where to Check Things**

| What You Want | Where to Look |
|---------------|---------------|
| **All leads** | Download `leads.csv` from your dashboard |
| **Live conversations** | Your personal phone (monitoring texts) |
| **Call history** | Twilio Console → Monitor → Logs → Calls |
| **SMS history** | Twilio Console → Monitor → Logs → Messages |
| **System status** | Visit: `https://yourcompany-bot.onrender.com/` (should say "running") |

---

## **Monthly Costs (Estimate)**

| Service | Cost |
|---------|------|
| Twilio Phone Number | $1-2/month |
| Twilio Usage (100 calls/texts) | $5-10/month |
| Google Gemini API | **FREE** (up to 1500 requests/day) |
| Render Hosting | **FREE** (basic tier) |
| **TOTAL** | **~$6-12/month** |

*Compare to: Hiring a receptionist at $2,000+/month*

---

## **Common Questions**

### **"What if I want to take over the conversation?"**
Just reply directly to the customer's text. They'll get your personal reply.

### **"Can I change what the AI says?"**
Yes! We can adjust Sarah's personality, scripts, and responses anytime.

### **"What if the AI gives wrong information?"**
Sarah is programmed to NEVER make up prices or guarantees. She only collects info and says you'll call them.

### **"Can I turn it off?"**
Yes. Just go to Twilio → Your Number → Delete the webhook URLs. Instant off.

### **"What happens if my phone is off?"**
Calls still trigger the auto-text. Texts still get AI replies. You just won't get monitoring messages until your phone is back on.

### **"Do I need to keep my computer running?"**
No. Once deployed to Render, it runs on the cloud 24/7 automatically.

---

## **Testing Your System (5 Minutes)**

### **Test 1: Missed Call Auto-Text**
1. Call your Twilio number from a friend's phone
2. Don't answer (let it ring 20 seconds)
3. Friend should receive: "Sorry I missed you! I'm on a roof right now..."

### **Test 2: AI Chat**
1. Text your Twilio number: "I need a roof inspection"
2. You should get Sarah's reply instantly
3. Your personal phone gets the monitoring message

### **Test 3: Call Forwarding**
1. Call your Twilio number from a verified phone
2. Your personal phone should ring
3. Answer it - conversation works normally

---

## **Getting Help**

**Technical Issues:**
- Contact us: [your support email/phone]
- We monitor the system and fix problems within 24 hours

**Twilio Account Problems:**
- Twilio Support: [support.twilio.com](https://support.twilio.com)
- Usually very fast (1-2 hours)

**Want to Change Something:**
- Contact us with your request
- Most changes done same day

---

## **Quick Reference Card** (Print This!)

```
┌─────────────────────────────────────────┐
│   AI RECEPTIONIST QUICK REFERENCE       │
├─────────────────────────────────────────┤
│                                         │
│  Your Twilio Number: _______________    │
│                                         │
│  Bot Dashboard:                         │
│  https://__________________________.com │
│                                         │
│  Twilio Console:                        │
│  twilio.com/console                     │
│                                         │
│  Check Leads:                           │
│  Download leads.csv from dashboard      │
│                                         │
│  Support: ____________________          │
│                                         │
│  Emergency Off Switch:                  │
│  Twilio → Phone → Delete webhooks       │
│                                         │
└─────────────────────────────────────────┘
```

---

## **Next Steps**

✅ **Step 1:** Share your Twilio credentials and personal phone with us

✅ **Step 2:** We deploy your bot (takes 10 minutes)

✅ **Step 3:** You test it with the steps above

✅ **Step 4:** Go live and start capturing leads 24/7!

---

**Questions?** Contact us anytime. We're here to help your business grow! 🚀
