"""Builds the games privacy policy pages (privacy-android.html, privacy-ios.html) from about.html's shared
header, mobile menu and footer, so they always match the rest of the site. Re-run after editing the text below.

usage: python tools/build_privacy.py
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPDATED = 'November 13, 2026'
CONTACT = 'varun@stellarisxr.com'


def chrome():
    src = open(os.path.join(ROOT, 'about.html'), encoding='utf-8').read()
    start = src.index('<body>')
    main_start = src.index('<main id="main">')
    main_end = src.index('</main>') + len('</main>')
    end = src.index('</html>') + len('</html>')
    top = src[start:main_start].replace(' aria-current="page"', '')
    bottom = src[main_end:end]
    return top, bottom


HEAD = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>{title} | Stellaris XR Studios</title>
    <meta name="description" content="{desc}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://stellarisxr.com/{file}" />

    <link rel="icon" type="image/png" href="assets/favicon.png" />
    <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,600&display=swap" rel="stylesheet" />

    <link rel="stylesheet" href="styles.css" />
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
</head>

'''


def page(file, title, desc, kicker, heading, other_file, other_label, body):
    top, bottom = chrome()
    main = f'''<main id="main">

        <section class="section dark legal">
            <div class="container legal-col">
                <p class="t-kicker">{kicker}</p>
                <h1 class="t-h1">{heading}</h1>
                <p class="legal-meta">Last updated {UPDATED}. Also available: <a href="{other_file}">{other_label}</a>.</p>
{body}
            </div>
        </section>

    </main>'''
    html = HEAD.format(title=title, desc=desc, file=file) + top + main + bottom + '\n'
    open(os.path.join(ROOT, file), 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', file)


def section(h, *paras):
    return f'                <h2>{h}</h2>\n' + ''.join(f'                {p}\n' for p in paras)


def common_intro(store, games_rows):
    return section(
        'Who we are',
        f'<p>Stellaris XR Studios ("we", "us") is an independent game studio in Halifax, Nova Scotia, Canada. '
        f'This policy explains what information our mobile games distributed through {store} collect, why, '
        f'who receives it and the choices you have. Questions or requests: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>',
        '<p>It covers these games:</p>',
        '<div class="legal-table"><table><thead><tr><th>Game</th><th>Status</th><th>Services used</th></tr></thead><tbody>'
        + games_rows + '</tbody></table></div>',
    ) + section(
        'The short version',
        '<ul>'
        '<li>Our games have no accounts and we run no servers. We do not see, store or sell your personal information.</li>'
        '<li>Your game progress is saved only on your device (and in your own device backup, if you have backup turned on).</li>'
        '<li>Ads are provided by Google AdMob, which uses device identifiers to show and measure ads. Where the law requires it, '
        'we ask for your consent first and you can change your choice at any time in the game\'s Settings.</li>'
        '<li>Purchases are handled entirely by the store. We never receive your payment details.</li>'
        '</ul>',
    )


ANDROID_ROWS = ('<tr><td>Sporelight</td><td>Android, Google Play</td>'
                '<td>Google AdMob, Google User Messaging Platform, Google Play Billing, Google Play Games Services</td></tr>')
IOS_ROWS = ('<tr><td>Sporelight</td><td>iOS version in development</td>'
            '<td>Google AdMob, Google User Messaging Platform, Apple In-App Purchase, Apple Game Center</td></tr>')

RIGHTS = section(
    'Your rights',
    '<p>Depending on where you live (for example the EU, UK, Canada, Quebec or a US state with a privacy law) you may have '
    'the right to access, correct, delete or move personal information, to object to or restrict processing, to withdraw '
    'consent and to opt out of targeted advertising or the "sale" or "sharing" of personal information. Because we do not '
    'hold personal information about players, most requests are best made directly to the provider that holds it '
    '(Google or Apple, linked above), and you can always change ad consent in the game. We are happy to help: email '
    f'<a href="mailto:{CONTACT}">{CONTACT}</a> and we will reply within 30 days. You may also complain to your local data '
    'protection authority, or in Canada to the Office of the Privacy Commissioner of Canada.</p>',
    '<p>We do not sell personal information for money. Showing personalised ads through AdMob may count as "sharing" or '
    'targeted advertising under some US state laws; you can opt out through the game\'s ad privacy choices or your '
    'device settings described above.</p>',
)

TAIL = section(
    'Legal bases (EU and UK players)',
    '<p>Personalised advertising and the related use of device identifiers rely on your <strong>consent</strong>, collected '
    'through Google\'s consent message. Showing non-personalised ads, preventing ad fraud, processing purchases and saving '
    'progress rely on our <strong>legitimate interests</strong> in running a free, ad-supported game and on '
    '<strong>performing our contract</strong> with you when you buy something.</p>',
) + RIGHTS + section(
    'Children',
    '<p>Our games are intended for players aged 13 and over and are not directed at children under 13. We do not knowingly '
    'collect personal information from children. If you believe a child has provided information through one of our games, '
    f'contact <a href="mailto:{CONTACT}">{CONTACT}</a> and we will help remove it.</p>',
) + section(
    'Retention, transfers and security',
    '<p>We keep no player data on our own systems. Information collected by Google or Apple is kept for the periods described in '
    'their privacy policies and may be processed in the United States and other countries where they operate, under the '
    'safeguards described in those policies. All communication between the game and these services is encrypted in transit.</p>',
) + section(
    'Changes',
    '<p>If our games start using a new service or collecting different information, we will update this page and the "last '
    'updated" date before that version is released.</p>',
) + section(
    'Contact',
    f'<p>Stellaris XR Studios, Halifax, Nova Scotia, Canada. Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>',
)


def android():
    body = common_intro('Google Play on Android', ANDROID_ROWS) + section(
        'Information stored on your device',
        '<p>Game progress, settings, unlocked items and purchase status are saved in a file on your device. It is not sent to us. '
        'If Android backup is turned on for your Google account, Android may include this file in your backup so progress can be '
        'restored on a new device; that backup is stored by Google under your account. Uninstalling the game deletes the file '
        'from the device.</p>',
    ) + section(
        'Advertising: Google AdMob',
        '<p>Free versions of our games show ads served by Google AdMob. To deliver, measure and limit ads and to prevent fraud, '
        'the AdMob SDK may collect your device\'s <strong>advertising ID</strong>, IP address (used to estimate a rough location), '
        'device and operating system information, app interactions with ads, and diagnostic data. Whether ads are personalised '
        'depends on your consent where it is required, and on your device settings.</p>',
        '<p>Learn more: <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google '
        'uses information from sites or apps that use its services</a> and the '
        '<a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a>.</p>',
    ) + section(
        'Consent: Google User Messaging Platform',
        '<p>If you are in the European Economic Area, the United Kingdom, Switzerland or a US state with a privacy law, the game '
        'shows Google\'s consent message before any ads load. You can review or change your choice at any time from '
        '<strong>Settings &gt; Ad privacy choices</strong> in the game. Until a choice is recorded where one is required, no ads '
        'are requested.</p>',
    ) + section(
        'Purchases: Google Play Billing',
        '<p>In-app purchases (for example, removing ads) are processed by Google Play. Google handles your payment details; the game '
        'only receives confirmation of what you own so it can unlock it, and checks that status again when the game starts so '
        'refunds are respected. See the <a href="https://payments.google.com/payments/apis-secure/u/0/get_legal_document?ldo=0&amp;ldt=privacynotice" '
        'target="_blank" rel="noopener">Google Payments privacy notice</a>.</p>',
    ) + section(
        'Leaderboards and achievements: Google Play Games Services',
        '<p>If you sign in to Google Play Games, Google receives your Play Games profile (player ID and gamer name), your leaderboard '
        'scores and achievements so they can be shown to you and, depending on your Play Games profile settings, to other players. '
        'Signing in is optional; the game is fully playable without it. Manage this in the Google Play Games app.</p>',
    ) + section(
        'Crash and performance data',
        '<p>If you have chosen to share usage and diagnostics with Google on your device, Google Play may collect crash reports and '
        'performance data for our games and show us aggregated, anonymised statistics. We do not use any other analytics.</p>',
    ) + section(
        'Your choices on Android',
        '<ul>'
        '<li><strong>Ad consent:</strong> Settings &gt; Ad privacy choices in the game (shown where the law requires it).</li>'
        '<li><strong>Advertising ID:</strong> Android Settings &gt; Privacy &gt; Ads (or Google &gt; Ads) to reset or delete it; '
        'without it, ads are not personalised.</li>'
        '<li><strong>Fewer ads:</strong> the one-time PRO purchase removes banner and between-level ads.</li>'
        '<li><strong>Play Games:</strong> sign out or delete Play Games data in the Google Play Games app.</li>'
        '<li><strong>Delete local data:</strong> uninstall the game, or clear its storage in Android Settings &gt; Apps.</li>'
        '</ul>',
    ) + TAIL
    page('privacy-android.html', 'Games Privacy Policy (Android)',
         'Privacy policy for Stellaris XR Studios mobile games on Google Play, including Sporelight.',
         'Games privacy policy', 'Android games', 'privacy-ios.html', 'iOS games policy', body)


def ios():
    body = common_intro('the Apple App Store on iPhone and iPad', IOS_ROWS) + section(
        'Information stored on your device',
        '<p>Game progress, settings, unlocked items and purchase status are saved in a file on your device. It is not sent to us. '
        'If iCloud Backup or a computer backup is turned on, iOS may include this file in your backup so progress can be restored; '
        'that backup is stored by Apple under your Apple Account or on your computer. Deleting the game removes the file from the device.</p>',
    ) + section(
        'Advertising: Google AdMob and App Tracking Transparency',
        '<p>Free versions of our games show ads served by Google AdMob. To deliver, measure and limit ads and to prevent fraud, the '
        'AdMob SDK may collect your IP address (used to estimate a rough location), device and operating system information, app '
        'interactions with ads, and diagnostic data. iOS asks your permission before any app can use your device\'s '
        '<strong>advertising identifier (IDFA)</strong> to track you across other companies\' apps and websites. If you choose '
        '"Ask App Not to Track", the IDFA is not available and ads are not personalised using it.</p>',
        '<p>Learn more: <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google '
        'uses information from sites or apps that use its services</a> and the '
        '<a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a>.</p>',
    ) + section(
        'Consent: Google User Messaging Platform',
        '<p>If you are in the European Economic Area, the United Kingdom, Switzerland or a US state with a privacy law, the game '
        'shows Google\'s consent message before any ads load, followed where applicable by Apple\'s tracking permission prompt. You '
        'can review or change your choice at any time from <strong>Settings &gt; Ad privacy choices</strong> in the game.</p>',
    ) + section(
        'Purchases: Apple In-App Purchase',
        '<p>In-app purchases (for example, removing ads) are processed by Apple. Apple handles your payment details; the game only '
        'receives confirmation of what you own so it can unlock it, and checks that status again when the game starts so refunds are '
        'respected. See the <a href="https://www.apple.com/legal/privacy/" target="_blank" rel="noopener">Apple Privacy Policy</a>.</p>',
    ) + section(
        'Leaderboards and achievements: Apple Game Center',
        '<p>If you are signed in to Game Center, Apple receives your Game Center profile, your leaderboard scores and achievements so '
        'they can be shown to you and, depending on your Game Center settings, to friends or other players. Game Center is optional; '
        'the game is fully playable without it. Manage it in iOS Settings &gt; Game Center.</p>',
    ) + section(
        'Crash and performance data',
        '<p>If you have chosen to share analytics with app developers on your device, Apple may provide us with crash reports and '
        'aggregated usage statistics. We do not use any other analytics.</p>',
    ) + section(
        'Your choices on iOS',
        '<ul>'
        '<li><strong>Ad consent:</strong> Settings &gt; Ad privacy choices in the game (shown where the law requires it).</li>'
        '<li><strong>Tracking:</strong> iOS Settings &gt; Privacy &amp; Security &gt; Tracking, to allow or deny tracking for each app.</li>'
        '<li><strong>Personalised ads from Apple:</strong> iOS Settings &gt; Privacy &amp; Security &gt; Apple Advertising.</li>'
        '<li><strong>Fewer ads:</strong> the one-time PRO purchase removes banner and between-level ads.</li>'
        '<li><strong>Game Center:</strong> sign out in iOS Settings &gt; Game Center.</li>'
        '<li><strong>Delete local data:</strong> delete the game from your device.</li>'
        '</ul>',
    ) + TAIL
    page('privacy-ios.html', 'Games Privacy Policy (iOS)',
         'Privacy policy for Stellaris XR Studios mobile games on the Apple App Store, including Sporelight.',
         'Games privacy policy', 'iOS games', 'privacy-android.html', 'Android games policy', body)


if __name__ == '__main__':
    android()
    ios()
