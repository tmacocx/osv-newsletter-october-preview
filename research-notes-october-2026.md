# Research notes — October 2026 issue (T293 → T299)

Everything dated in **Deadline watch** and **The month ahead** was checked against the organizer's or agency's own page. T293 items were checked Sept 14, 2026; T299 re-checked the items marked below the same day and added the new ones. Items that could not be verified were left out and are listed at the end.

## T299 build pass — what changed and why

| # | Request | Done |
|---|---|---|
| 1 | Scrub process/narration lines; one verification line at the end of Deadline watch; hero ≠ subject; short subject | "Every listing was checked…", "Only dates we could confirm…", "Nothing here is a guess", the footer "details come from organizers' pages" line, and the old "Dates checked Sept 14, 2026 against the linked pages…" line are gone. The only verification line is **"Dates confirmed Sept 14. If something changed, reply and we will fix it."** Subject (in `<title>` and the head comment): **"October: sensory-friendly events + deadlines"** (44 chars). Hero stays "October in the Village". |
| 2 | Weekly groups as a stacked list, OSV Thursday first; brand-color phone; Thursday off the dated Oct 1 card; fix "begins" | "Every week" card is now two stacked rows, Thursday group first. Phone numbers are `tel:` links in the brand accent. The Oct 1 dated card is removed (the group is a regular weekly meeting, not a special session). Wording: "Meeting weekly since September, so join any Thursday." |
| 3 | Library: two cards, Therapy Styles then the grief guide | Two cards. Grief card links `/resources/grieving-the-life-you-imagined` with the published title "Grieving the life you imagined". Card copy is the site's own library blurb for each guide (see "Copy sources" below). |
| 4 | Deadline watch in four labeled groups; verify new items or omit; compress On the radar | Groups: **School** (fall break + conferences, ACT Nov 6), **Insurance** (Medicare OE, HealthCare.gov OE, Katie Beckett any time), **Money** (FAFSA Oct 1, COLA Oct 14, TN Promise Nov 2), **Community** (voter registration Oct 5 with early voting and absentee dates, clocks fall back Nov 1). On the radar is three one-liners (Angel Tree, EFS, IEA). |
| 5 | No Teams meeting ID/passcode; registration link only; pay-what-you-can incl. nothing everywhere | Meeting ID and passcode removed. The only Village Hall link is `/village-hall` ("Register for Village Hall"). "Pay what you can, including nothing" appears on the event card, the Q&A tie-in, the Village Hall intro, and the Village Hall block (with the $0 / $10 / $20 / $35 ladder from the live page). |
| 6 | View in browser + In this issue anchors; 3-line events; keep all 10 events; cut length | "View in browser" (`{$url}`) above the masthead; "In this issue" anchor line under the hero (`#events #deadlines #library #hope #question #village-hall`). Each event is title / logistics / sensory+link. All 10 events remain (9 dated + the Thursday group in the weekly list). Rendered height at 760px: 8,379px vs 8,514px before, even with the added note, contents line, second guide card, and sensory lines. |
| 7 | Taylor note above events, below hero | Peach card "A note from Taylor" between the contents line and The month ahead. **The body is a drafted placeholder** (her exact copy was not in the repo or the prior run); marked with an HTML comment. |
| 8 | Sensory line + drive time on every event | Every event has a bold **Sensory:** line and a drive time ("About 45 min", "In Murfreesboro", "No drive" for online). |
| 9 | Wall of Hope as invitation only | Section header "Wall of Hope", card "Borrow a little hope, or lend some", one link to `/hope`. No placeholder story. |
| 10 | Name Q&A recurring + submit link; keep parent-to-parent line under answer; drop footer duplicate | Intro: "Our recurring column: one real question from a local parent, answered plainly, every issue. Send us your question →" (`/contact`). Card eyebrow "October's question". "Parent-to-parent guidance, not legal advice." stays under the answer; the footer disclaimer sentence is removed. |
| 11 | Consistency/compliance | "Murfreesboro and surrounding areas" in the footer and the Wall of Hope card (the only remaining "Middle Tennessee" is in the organization name Down Syndrome Association of Middle Tennessee). Footer framing mirrors the live homepage: "built around autism, open to every kind of difference and disability." Real postal address of the owning entity. `{$unsubscribe}` one-click link. All text/background pairs ≥ 4.5:1 (table below). Dark-mode styles for Apple Mail/iOS/Outlook (`prefers-color-scheme`) and Outlook.com (`data-ogsc`/`data-ogsb`). Spooktacular says "Time and cost not posted yet" with the gym's phone. Separators are middots; no em dashes remain in the file. |

## Deadline watch — sources

| Group | Date | Item | Source read | What the source says |
|---|---|---|---|---|
| School | Oct 5–9 | Fall break, RCS and MCS | [RCS 2026–27 calendar](https://www.rcschools.net/o/rcs/page/rcs-academic-calendars); [MCS 2026–27 calendar PDF](https://resources.finalsite.net/images/v1775835497/cityschoolsnet/iomdoih1pjalvwrt6ln7/2026-27-MCS-School-Calendar.pdf) (T293) | RCS: fall break Oct 5–9, report cards Oct 16, conferences Tue Oct 20, no school Nov 3. MCS: fall break Oct 5–9; Nov 3 = conferences and report cards, no school for students. |
| School | Fri Nov 6 | ACT Dec 12: registration and accommodations deadline | [ACT test dates](https://www.act.org/content/act/en/products-and-services/the-act/registration/test-dates.html); [ACT accommodations](https://www.act.org/content/act/en/products-and-services/the-act/registration/accommodations.html) (T293) | Regular deadline Nov 6, late Nov 29; accommodations requests due by the regular deadline through the school official. |
| Insurance | Oct 15 – Dec 7 | Medicare open enrollment | [Medicare.gov](https://www.medicare.gov/health-drug-plans/open-enrollment); [TN SHIP](https://www.tn.gov/disability-and-aging/disability-aging-programs/tn-ship.html) (T293) | Oct 15 – Dec 7 each year; TN SHIP 1-877-801-0044. |
| Insurance | Nov 1 – Jan 15 | HealthCare.gov open enrollment | [Dates and deadlines](https://www.healthcare.gov/quick-guide/dates-and-deadlines/) (T293) | Nov 1 – Jan 15; enroll by Dec 15 for Jan 1. |
| Insurance | Any time | Katie Beckett | [TennCare Katie Beckett](https://www.tn.gov/tenncare/long-term-services-supports/katie-beckett-waiver.html) (T293) | Year-round applications; Part B waiting list. Linked to the OSV guide. Moved from "On the radar" into Insurance. |
| Money | Thu Oct 1 | 2027–28 FAFSA opens | [FSA announcement](https://financialaidtoolkit.ed.gov/tk/announcement-detail.jsp?id=fafsa-updates) (T293) | Available to everyone by Oct 1, 2026. TN Promise FAFSA deadline April 1. |
| Money | **Wed Oct 14** | **2027 Social Security / SSI COLA announced (new)** | [BLS CPI release schedule](https://www.bls.gov/schedule/news_release/cpi.htm); [BLS October 2026 schedule](https://www.bls.gov/schedule/2026/10_sched_list.htm); [SSA COLA page](https://www.ssa.gov/cola/) | September 2026 CPI releases **Wed Oct 14, 2026, 8:30 AM ET**; SSA announces the COLA the same morning and it applies to January payments. Worded as "expected the morning the September inflation report comes out." |
| Money | Mon Nov 2 | Tennessee Promise deadline | [CollegeforTN](https://www.collegefortn.org/tnpromise/); [tnAchieves](https://www.tnachieves.org/tn-promise) (T293) | Nov 2, 2026. |
| Community | Mon Oct 5 | Voter registration deadline, Nov 3 election | [TN SOS elections calendar](https://sos.tn.gov/elections/calendar) (**re-read Sept 14 for T299**) | "Voter Registration Deadline Monday, October 5, 2026 · Early Voting Wednesday, October 14 – Thursday, October 29, 2026 · Absentee Ballot Request Deadline Saturday, October 24, 2026." |
| Community | **Sun Nov 1** | **Clocks fall back (new)** | [NIST daylight saving time](https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst) | DST ends 2:00 AM on the first Sunday in November = Nov 1, 2026. The bedtime-shift sentence is parent-to-parent advice, not a claim about the source. |

### On the radar — sources

| Item | Source read | Status |
|---|---|---|
| Salvation Army Angel Tree (Rutherford & Cannon) | [Angel Tree page](https://www.salvationarmymurfreesboro.org/angeltree) (**re-read Sept 14 for T299**) | "Currently our applications are full… spots may open up." Adoptions Nov 6; gift drop-off Nov 6 – Dec 4. Moved from the dated list to On the radar (no date for families). |
| EFS 2027–28 | [EFS applications page](https://www.tn.gov/education/efs/applications.html); [2026–27 timeline PDF](https://www.tn.gov/content/dam/tn/education/efs/EFS_2026_27_Program_Timeline.pdf) (**re-checked Sept 14**) | 2027–28 dates "to be posted… when available." **Correction:** the 2026–27 window closed **Feb 6, 2026** (extended from Jan 30), so the email now says "Dec 9 to Feb 6." Oct 1 family office hours 1–2 PM CT confirmed on the EFS page. |
| IEA 2027–28 | [TDOE IEA page](https://www.tn.gov/education/iea.html) (T293) | Projected to open Feb 16, 2027. |

### Removed from the Deadline watch in T299

- "Tue Nov 3 · Election Day, no school" as its own row: already covered by the fall-break row (MCS conferences Nov 3, no school) and the voter row (Election Day Nov 3).
- The second link on the voter row (TN election calendar): GoVoteTN is the same office and the row was wrapping to a dangling separator.
- Toys for Tots (Rutherford County): no 2026 request dates published (only 2016 press). Omitted.

## The month ahead — event sources

| Date | Event | Source read | Sensory line comes from |
|---|---|---|---|
| Sat Oct 3 | Game Day · Autism Tennessee | [autismtn.org event](https://autismtn.org/events/EventDetails.aspx?id=2003814) (Cloudflare check blocks curl; verified in T293 and on the [OSV calendar](https://ourspecialvillagetn.com/events)) | Indoor games, registration required, food provided, all ages and families. |
| Sat Oct 10 | Village Hall | [ourspecialvillagetn.com/village-hall](https://ourspecialvillagetn.com/village-hall) (**re-read Sept 14**) | "Bring a question or simply listen." Lesson recorded, Q&A not. Pay-what-you-can ladder $0 / $10 / $20 / $35. **The live page still says "First guest TBD · Registration not open."** |
| Sun Oct 11 | Sensory Sunday Hour · Frist | [fristartmuseum.org](https://fristartmuseum.org/event/sensory-sunday-hour-5/) (**re-read**) | "Sound levels will be lowered… multisensory carts… stay into the afternoon for Family Sunday." Free for members and ages 18 and under. |
| Thu Oct 15 | All Access Night: Monsters in the Museum | [explorethedc.org](https://www.explorethedc.org/event/monsters-in-the-museum/) (**re-read**) | "Smaller crowds and reduced sensory stimulation… after hours… at their own pace… free, but registration is required." |
| Oct 16 – Nov 1 | Boo at the Zoo | [nashvillezoo.org/boo](https://www.nashvillezoo.org/boo) (**re-read**) | $19 Mon–Thu, $23 Fri–Sun (ages 2+), parking $10, tickets required; Zooper Packs (fidgets, earplugs) at the ticket booth; social story in English and Spanish; Mon–Wed least crowded; "after dark, some areas may be scary for young children." |
| Sat Oct 17 | Super Sports Saturday · ABLE Youth | [ableyouth.org](https://www.ableyouth.org/event/super-sports-saturday-34/) (**re-read**) | Adaptive sports and games, kids of all ages, RSVP info@ableyouth.org, Williamson County Recreation Center. No cost is published, so none is stated. |
| Sat Oct 24 | The EXTRA Mile · DSAMT | [somethingextra.org](https://somethingextra.org/ways-to-help/the-extra-mile/) (**re-read**) | 9 AM gates, bounce houses and food trucks open; 10 AM live music; rain or shine; no pets or balloons. |
| Sun Oct 25 | Sensory Spooktacular · We Rock the Spectrum | [werockthespectrummurfreesboro.com](https://werockthespectrummurfreesboro.com/) (**re-checked Sept 14**) plus web search | Still nothing published for 2026 (only 2025 listings). Email says "Time and cost not posted yet" and gives the gym's phone (615-962-8627, confirmed on their site). |
| Sat Oct 31 | Evergreen Trunk or Treat | [evergreenls.org/trunkortreat](https://evergreenls.org/trunkortreat/) (**re-read**) | Oct 31, 1–3 PM, 6050 Dana Way, Antioch, free, "for individuals with intellectual and/or developmental disabilities, families…" |
| Weekly Thu | OSV online parent group | [ourspecialvillagetn.com/group](https://ourspecialvillagetn.com/group) | Thursdays 7–8 PM, free, cameras optional, not recorded. **The live page and homepage still say "First meeting October 1, 2026"**; the email follows the build request ("started September"). |
| Weekly Wed | We Rock the Spectrum Wednesday group | [OSV calendar](https://ourspecialvillagetn.com/events) | 5:00 PM, led by Cari Parr, call for current details. |

### Drive times

Computed Sept 14 with OSRM (free-flow driving time, no traffic) from Murfreesboro Public Square, then rounded up to a round number and prefixed "About": Frist 42 min → 45; Nashville Zoo 35 → 35; Williamson County Rec Center 48 → 50; Ward Ag Center, Lebanon 41 → 40; Evergreen, Antioch 30 → 30; Game Day (Nashville, exact address sent after registration) ~43 → 45. Discovery Center and We Rock the Spectrum are in Murfreesboro; Village Hall is online ("No drive").

## Copy sources

- **Grief guide card**: title and blurb are the site's own library entry for [/resources/grieving-the-life-you-imagined](https://ourspecialvillagetn.com/resources/grieving-the-life-you-imagined): "Why grief after a diagnosis does not make you less affirming, what parents are really grieving, and how letting go of the expected story makes room for the child in front of you." If the build request has a different blurb, paste it verbatim.
- **Therapy Styles card**: the site's library blurb: "Two therapists can have the same license and run completely different rooms. Learn what the common labels actually look like."
- **Footer framing**: the live homepage: "An autism-focused resource hub for families in Murfreesboro and surrounding areas — built around autism, open to every kind of difference and disability."
- **Postal address**: Our Special Village is "owned and operated by Little Luminaries Therapy Services, PLLC" (site footer). The practice's published address is **1810 Ward Dr, Suite 101, Murfreesboro, TN 37129** ([littleluminariestn.com/contact](https://www.littleluminariestn.com/contact)). Swap in a different mailing address if OSV prefers one.
- **Taylor note**: drafted placeholder in her voice. Replace with her exact copy.
- **Q&A steps**: unchanged from T293 (TDOE dispute-resolution page, Administrative Complaint Manual, Timelines in Special Education; STEP TN and DRT numbers match the OSV IEP & 504 guide).

## Accessibility and rendering

Contrast (WCAG 2.x, all body/label sizes):

| Pair | Ratio |
|---|---|
| Body `#4a5169` on white / cream `#f7f1e2` / peach `#f6e4d6` | 7.9 / 7.0 / 6.4 |
| Headings `#1b2340` on white / peach | 15.4 / 12.5 |
| Links and eyebrows `#964720` (was `#a9552a`, which was 4.2 on peach) on white / cream / peach | 6.2 / 5.6 / 5.3 |
| Fine print `#6b6250` (was `#8a7f6a`, 3.5) on cream / white | 5.3 / 6.0 |
| Gold eyebrow `#d4ac4d`, sand `#ded7c4`, cream `#f7f1e2` on navy `#1b2340` | 7.2 / 10.7 / 13.7 |
| Button text `#1b2340` on gold `#d4ac4d` | 7.2 |
| Dark mode: body `#d5d2c8`, headings `#f3efe4`, links `#f0b27a` on card `#1f2740` / tint `#2a2438` / page `#151a2b` | ≥ 7.0 everywhere |

Dark mode: `@media (prefers-color-scheme: dark)` overrides on `.os-*` classes (page, cards, tints, badges, text, links, buttons, section-icon chips), plus `[data-ogsc]`/`[data-ogsb]` equivalents for Outlook.com. Gmail ignores both and auto-inverts; the palette survives inversion because every text/background pair is set explicitly.

Rendering: headless Chrome at 390px and 760px, light and dark. No horizontal overflow; links wrap between labels, not inside them; masthead stays on one line at 390px. Tag balance verified. All `href`/`src` return 200 except the known bot-check hosts (autismtn.org, evergreenls.org, ssa.gov, all confirmed by browser fetch) and tn.gov (times out for curl, pages confirmed by fetch/search).

MailerLite: `{$url}` (view in browser) and `{$unsubscribe}` (one-click unsubscribe) are the platform's link variables and only resolve inside MailerLite; List-Unsubscribe headers are added by the platform at send.

## Considered and left out

- Sensory Sessions with Love Learning Music, Linebaugh Library (1st Saturdays on the OSV calendar): the library's own calendar still shows no October date; October URLs 404. Left out.
- Special Needs Family Fall Fest, Pegram (Oct 29): no organizer link; ~60 miles. Left out.
- Toys for Tots (Rutherford County): no 2026 request window published. Left out.
- Vanderbilt TRIAD October sessions: provider-facing. Left out.
- General trunk-or-treats and fall festivals sourced only via aggregators. Left out.

## Editor to-dos before send

1. **Paste Taylor's exact note** into the "A note from Taylor" card (drafted placeholder now; see HTML comment).
2. Confirm the grief-guide blurb matches the one she gave; the card currently uses the site's library blurb.
3. Update ourspecialvillagetn.com/village-hall (still "First guest TBD · Registration not open") and /group + homepage (still "First meeting October 1, 2026") so they match the email.
4. Re-check We Rock the Spectrum for Spooktacular time/cost; replace "Time and cost not posted yet" if published.
5. Confirm the footer mailing address (Little Luminaries, 1810 Ward Dr, Suite 101) is the one OSV wants on the newsletter.
6. If Angel Tree registration reopens, promote it back into Money with the date.
