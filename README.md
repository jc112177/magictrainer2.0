# Tabletop Mage: install it as an app & publish it

This folder is the complete app. It works on PC (Chrome/Edge), Android phones and tablets.
Everything below is **free**, except the Google Play route (explained in step 4).

## 1. Put it online for free (GitHub Pages, no credit card)
1. Make a free account at https://github.com.
2. Click **New repository** and name it exactly `YOURNAME.github.io` (your GitHub username).
   Using that exact name puts the app at the root of your site, which you need for step 3.
3. Click **uploading an existing file**. Drag in **everything** from this folder:
   index.html, manifest.webmanifest, sw.js, the icon PNGs, and the hidden `.nojekyll` file.
   Then click **Commit changes**.
4. Go to **Settings → Pages**. Under "Branch" pick `main` and `/ (root)`, then **Save**.
5. After a minute or two your app is live at **https://YOURNAME.github.io**

## 2. Install it on Android (and on a PC)
- **Android:** open your link in **Chrome** and tap **📲 Install app** in the top bar
  (or tap ⋮ → **Install app** / **Add to Home screen**). It gets its own icon and opens full screen
  like a normal app. Card images you've already seen stay cached, so they load instantly.
- **PC:** open the link in Chrome or Edge and click the install icon in the address bar
  (or the 📲 button in the app).
- **Voice tip:** on phones the coach uses your phone's built-in Google voice by default. You can
  switch to the natural AI voice in ⚙ Settings, but it's a one-time ~90 MB download, so use Wi-Fi.

## 3. Make a real Android app file (APK), free
1. Go to https://www.pwabuilder.com, paste your link, and click **Start**.
2. Click **Package for stores → Android → Generate**. Download the zip. It contains a signed
   `.apk`, an `.aab`, an `assetlinks.json` file, and your **signing key** (back the key up and keep
   it private: you need it for every future update).
3. In your GitHub repo, create the file `.well-known/assetlinks.json` and paste in the contents of
   the `assetlinks.json` from the zip. This tells Android that the app and your website belong
   together, so the app opens full screen with no browser address bar.
4. Copy the `.apk` to your phone and open it. Allow "install unknown apps" when asked.
   You can also share the APK with friends.
   - Heads-up: Google is rolling out "developer verification" for sideloaded apps (four countries
     in Sept 2026, then globally from 2027). Google says it will offer a **free** "limited
     distribution" account for hobbyists (up to 20 devices, email only). Until then, sideloading
     in the US works as usual.

## 4. Google Play Store: what it really takes (not free)
- **One-time $25 registration fee**, plus identity verification.
- New **personal** accounts (created after Nov 13, 2023) must run a **closed test with at least
  12 testers who stay opted in for 14 days in a row** before they can publish publicly.
- If you decide to do it later: create a Play Console account, upload the `.aab` from PWABuilder to
  a **Closed testing** track, invite 12+ testers by email, wait 14 days, then apply for production
  access. Also replace `assetlinks.json` with the version shown in Play Console → Setup → App
  integrity, because Google re-signs your app.

## 5. Free ways to share it
- **Your GitHub Pages link** (step 1): anyone can open it and install it. This is the easiest option.
- **itch.io**: free to upload. Zip this folder and upload it as an HTML5 game so people can play in
  the browser, and attach the APK as a download.
- Note: the Amazon Appstore for Android phones shut down on Aug 20, 2025 (it now serves only Fire
  devices).

## 6. Important: the card artwork belongs to Wizards of the Coast
The card images and the *Magic: The Gathering* name are owned by Wizards of the Coast. Fan projects
are allowed under the **Wizards Fan Content Policy** if they stay **free**: no ads, no paywalls, no
"official" claims. The app already shows the required disclaimer on its home screen.
- Don't charge money or add ads.
- App stores may still reject apps that use another company's trademarks or artwork. That's another
  reason the free website/APK routes above are the safest.
- Card data comes from Scryfall's free API. Keep it free and credit Scryfall (already done).
(This isn't legal advice. Read https://company.wizards.com/en/legal/fancontentpolicy yourself.)
