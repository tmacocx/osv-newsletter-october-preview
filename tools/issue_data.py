"""Words, dates and pictures for the Nov 2026 - Feb 2027 issues (layout lives in build-issues.py).

Sources:
- Events: ourspecialvillagetn.com public/data/events.json (updated 2026-09-26) unless a row's
  comment names the organizer page it was verified on.
- Deadlines: official pages listed in research-notes-nov-2026-feb-2027.md.
- Guides, blurbs and question answers: the site's own guide pages and library cards.
- ph("...") marks a placeholder Taylor still has to fill in; it shows as a dashed yellow box.
"""

SITE = "https://ourspecialvillagetn.com"
PH_OPEN, PH_CLOSE = "⟦", "⟧"


def ph(text):
    return f"{PH_OPEN}{text}{PH_CLOSE}"


VH_TIME = "9:30 to 11:00 AM Central"
VH_ABOUT = ("A 45-minute lesson with the guest, then live parent questions. The lesson is recorded "
            "and sent to registrants; the Q&amp;A is not.")
HOPE_QUOTE = ph("A parent&rsquo;s story from the Wall of Hope goes here: two to four sentences, shared with permission.")
HOPE_WHO = ph("First name") + ", Murfreesboro"  # Taylor: every Wall of Hope signs off name, Murfreesboro

RECESS_META = ("8:00&ndash;11:45 AM &middot; Otter Creek Church, Brentwood &middot; "
               "Respite for kids with disabilities and their siblings &middot; About 40 min")
RECESS_LINK = ("mailto:rebecca.whitaker@ottercreek.org", "Email to reserve a spot")
GAME_DAY_META = ("12:00&ndash;3:00 PM &middot; Nashville &middot; Food provided, registration required "
                 "&middot; About 45 min")
GAME_DAY_LINK = ("https://autismtn.org/events/EventDetails.aspx?id=2003814", "Register")
LINEBAUGH_META = ("11:00 AM&ndash;12:00 PM &middot; Linebaugh Public Library, Murfreesboro &middot; "
                  "Low-stimulation music activities")
LINEBAUGH_LINK = ("https://rclstn.org/events/", "Library calendar")
TEEN_CONNECT_META = ("6:00&ndash;8:00 PM &middot; Nashville &middot; Free peer group for neurodivergent "
                     "teens 14&ndash;17, registration required &middot; About 45 min")
TEEN_CONNECT_LINK = ("https://autismtn.org/events/EventDetails.aspx?id=2065883", "Register")

VH_TBD = dict(
    date=ph("Saturday date to come"),
    time=ph("Time to come"),
    topic=ph("Topic to come"),
    guest=None,
    guest_placeholder=ph("Guest expert to be announced. Add name, role, photo, and a short bio once booked."),
    about=VH_ABOUT,
    button="Get Village Hall details",
    art_alt="The village square in winter: the courthouse, a gazebo, and shops along a snowy path.",
)

ISSUES = [
    # ------------------------------------------------------------------ November 2026
    dict(
        id="2026-11", send_on="2026-11-01", month="November", month_year="November 2026",
        subject="November: AAC round table + sensory-friendly events",
        preheader=("An AAC round table with PRC-Saltillo and Tobii Dynavox, Thanksgiving break dates, sensory-friendly "
                   "events, and two guides on AAC devices and Katie Beckett funds."),
        hero_alt="Illustration of the village in autumn: homes, shops, and neighbors walking the path.",
        note=[
            ("This month&rsquo;s Village Hall is one I have been looking forward to! I will be joining Amanda "
             "Rains of PRC-Saltillo and Kerry Hankins-Grider with Tobii Dynavox for an AAC round table on "
             "Saturday, November 14. Amanda is a speech-language pathologist and LAMP Certified Professional "
             "who has spent her career helping children and young adults communicate with AAC. "
             + ph("One or two sentences introducing Kerry (bio coming).")),
            ("AAC can be more than just for people who are nonverbal or nonspeaking. Many autistic kids and "
             "adults lose access to language when they are dysregulated, and a device can help in those moments "
             "or simply give them more confidence. Whether your child uses a device every day or you are "
             "wondering if AAC could help, bring your questions."),
            ("Thanksgiving can be a lot for our kids and for us. Whatever your table looks like this year, "
             "I hope you find a little room to rest."),
        ],
        note_highlight="a little room to rest",
        chips=[("#deadlines", "Thanksgiving break"), ("#village-hall", "AAC round table"),
               ("#events", "Sensory-friendly events"), ("#library", "AAC + funding guides")],
        three_things=[],       # filled from research below
        all_deadlines=[],
        confirmed="",
        deadlines_meta="",
        village_hall=dict(
            date="Saturday, November 14, 2026",
            time=VH_TIME,
            topic="AAC round table with Taylor, PRC-Saltillo, and Tobii Dynavox",
            guests=[
                dict(
                    name="Amanda Rains, M.S., CCC-SLP",
                    role="LAMP Certified Professional &middot; PRC-Saltillo",
                    photo="amanda-rains-160.jpg",
                    photo_alt="Amanda Rains, M.S., CCC-SLP.",
                    bio=("Amanda has focused on AAC since graduate school, where she led an AAC group for adults "
                         "with Down syndrome. In private practice she ran AAC evaluations and therapy for children "
                         "and young adults who use AAC, and coached families and school teams to make devices work "
                         "every day. She is a LAMP Certified Professional with PRC-Saltillo."),
                ),
                dict(
                    name="Kerry Hankins-Grider",
                    role="Tobii Dynavox",
                    photo=None,
                    photo_alt="Kerry Hankins-Grider.",
                    bio=ph("Kerry&rsquo;s bio goes here (bio coming)."),
                ),
            ],
            about=("A conversation about AAC: who it can help, how families choose and fund a device, and how to "
                   "make it part of everyday life. Then live parent questions. The talk is recorded and sent to "
                   "registrants; the Q&amp;A is not."),
            art_alt="The Village Hall with its doors open, neighbors seated outside listening to a speaker.",
        ),
        events=dict(
            featured=dict(
                title="Sensory Sessions with Love Learning Music &middot; Linebaugh Library",
                meta="Sat Nov 7 &middot; 11:00 AM&ndash;12:00 PM &middot; Murfreesboro",
                blurb="Low-stimulation music activities, plus information about local music-therapy resources.",
                link=LINEBAUGH_LINK,
                art_alt="Families walking through the village in autumn, one child in a wheelchair and one with a service dog.",
            ),
            list=[
                dict(chip=("Sat", "7", "Nov"), title="rEcess &middot; Otter Creek Church and 99 Balloons",
                     meta=RECESS_META, link=RECESS_LINK),
                dict(chip=("Sat", "7", "Nov"), title="Game Day &middot; Autism Tennessee",
                     meta=GAME_DAY_META, link=GAME_DAY_LINK),
                dict(chip=("Thu", "12", "Nov"), title="Teen Connect &middot; Autism Tennessee",
                     meta=TEEN_CONNECT_META, link=TEEN_CONNECT_LINK),
                dict(chip=("Mon", "16", "Nov"),
                     title="Daily Living Skills for Autistic Teens and Young Adults &middot; Vanderbilt Kennedy Center",
                     meta="12:00&ndash;1:00 PM &middot; Nashville or online",
                     link=("https://vkc.vumc.org/events/7214", "Details")),
                dict(chip=("Sat", "21", "Nov"), title="Super Sports Saturday &middot; ABLE Youth",
                     meta=("9:00 AM&ndash;12:00 PM &middot; Williamson County Rec Center, Franklin &middot; "
                           "Adaptive sports, RSVP required &middot; About 45 min"),
                     link=("https://www.ableyouth.org/event/super-sports-saturday-35/", "Details")),
                # Verified Sept 28 on nashvillesymphony.org/America + /sensoryfriendly and nashvillezoo.org/glow-wild.
                dict(chip=("Sun", "15", "Nov"), title="Sensory-friendly symphony + Glow Wild &middot; Nashville",
                     meta=("Nashville Symphony family concert Sun Nov 15, 3:00 PM, with quiet spaces, headphones and "
                           "fidgets. Nashville Zoo lights nightly from Nov 13, free sensory kits; 5 PM is quietest."),
                     links=[("https://www.nashvillesymphony.org/America", "Symphony"),
                            ("https://www.nashvillezoo.org/glow-wild", "Glow Wild")]),
            ],
            calendar_label="View the full November events calendar",
        ),
        library_title="From the library",
        guides=[
            dict(label="Communication", title="AAC devices and how to get one",
                 blurb=("Evaluations, funding, free device trials, and the systems compared: the full path to "
                        "a reliable way to communicate."),
                 path="/resources/aac-devices",
                 art_alt="A therapy clinic and an open porch where a child and adults use a tablet together, in autumn."),
            dict(label="Paying for care", title="Using your Katie Beckett funds",
                 blurb=("Practical Tennessee Katie Beckett Part B ideas for therapy, respite, equipment, supplies, "
                        "activities, and documentation."),
                 path="/resources/katie-beckett-funds", cta="Read the funds guide",
                 art_alt="A family crossing a stone footbridge toward a brick office building in autumn."),
        ],
        hope=dict(quote=HOPE_QUOTE, who=HOPE_WHO,
                  art_alt="Neighbors pinning notes of hope to a wall in the village, with autumn trees around it."),
        question=dict(
            q="Will using an AAC device stop my child from learning to talk?",
            short=("Almost every parent worries about this, and the evidence points the other way: children "
                   "given a reliable way to communicate tend to speak more, not less. AAC is not only for kids "
                   "with no words; many autistic kids lose language when they are dysregulated, and a device "
                   "can carry them through."),
            steps=[
                ("Start without waiting.", "There is no readiness test and no age floor. A picture board on the "
                 "fridge counts, and nobody has to approve it first."),
                ("Model, don&rsquo;t quiz.", "Point to &ldquo;more&rdquo; as you say &ldquo;more.&rdquo; Then wait "
                 "longer than feels polite; the answer at second eight still counts."),
                ("Keep it close.", "At dinner, in the car, at Grandma&rsquo;s. Never take AAC away as a "
                 "consequence: it is a voice, not a privilege."),
            ],
            links=[(f"{SITE}/resources/what-is-aac", "What is AAC?"),
                   (f"{SITE}/resources/aac-devices", "Getting a device")],
            disclaimer="Parent-to-parent guidance, not medical advice.",
        ),
        group_line="Thursdays, off Thanksgiving (Nov 26)",
        todo=[],
    ),
    # ------------------------------------------------------------------ December 2026
    dict(
        id="2026-12", send_on="2026-12-01", month="December", month_year="December 2026",
        subject="December: winter break dates + a sensory-friendly Santa",
        preheader=("Winter break dates, a sensory-friendly Santa morning, a guide for running on empty, "
                   "and one holiday question answered."),
        hero_alt="Illustration of the village in winter: snowy homes, shops, and neighbors walking the path.",
        note=[
            ("December is full: school programs, parties, travel, and gatherings that can stretch every "
             "nervous system in the house, including yours."),
            ("This issue keeps it simple: the dates to know before winter break, a sensory-friendly Santa "
             "morning in Cool Springs, and a guide for the days you are running on empty. At Village Hall on "
             "Saturday, December 12, Katie Dell of Behavior Cubed joins us for all things behavior."),
            ("However your family celebrates, or doesn&rsquo;t, I hope the season gives you a few quiet "
             "moments that are just yours."),
        ],
        note_highlight="a few quiet moments that are just yours",
        chips=[("#deadlines", "Winter break"), ("#events", "Sensory-friendly Santa"),
               ("#library", "Guides for full days"), ("#question", "Holiday gatherings")],
        three_things=[], all_deadlines=[], confirmed="", deadlines_meta="",
        village_hall=dict(
            VH_TBD,
            date="Saturday, December 12, 2026",
            time=VH_TIME,
            topic="All things behavior",
            guests=[dict(
                name="Katie Dell",
                role="Neurodiversity-affirming BCBA &middot; Behavior Cubed",
                photo=None,
                photo_alt="Katie Dell.",
                bio=ph("Katie&rsquo;s credentials, photo, and a short bio."),
            )],
        ),
        events=dict(
            featured=dict(
                title="Santa&rsquo;s Sensory Wonderland &middot; Mindful Voices Autism Advocacy",
                meta="Sat Dec 12 &middot; 10:00 AM&ndash;1:00 PM &middot; Marriott Cool Springs",
                blurb="A sensory-friendly Santa morning with local family resources. About 40 minutes from Murfreesboro.",
                link=(f"{SITE}/events", "Details on our calendar"),
                art_alt="Families walking through the snowy village, one child in a wheelchair and one with a service dog.",
            ),
            list=[
                dict(chip=("Sat", "5", "Dec"), title="Sensory Sessions with Love Learning Music &middot; Linebaugh Library",
                     meta=LINEBAUGH_META, link=LINEBAUGH_LINK),
                dict(chip=("Sat", "5", "Dec"), title="rEcess &middot; Otter Creek Church and 99 Balloons",
                     meta=RECESS_META, link=RECESS_LINK),
                dict(chip=("Sat", "5", "Dec"), title="ABLE Youth Christmas Party",
                     meta=("11:00 AM&ndash;2:00 PM &middot; Berry&rsquo;s Chapel Church of Christ, Franklin "
                           "&middot; RSVP required &middot; About 45 min"),
                     link=("https://www.ableyouth.org/event/able-youth-christmas-party-4/", "Details")),
            ],
            calendar_label="View the full December events calendar",
        ),
        library_title="From the library",
        guides=[
            dict(label="Parent well-being", title="When your nervous system is full",
                 blurb=("Understand co-regulation, notice your own overload sooner, and build a realistic plan "
                        "for staying steady enough, or repairing when you cannot."),
                 path="/resources/when-your-nervous-system-is-full",
                 art_alt="A parent and child walking a snowy path toward a small house with a signpost and bench."),
            dict(label="Planning ahead", title="Planning for adulthood and for when you&rsquo;re gone",
                 blurb=("Trusts, ABLE accounts, letters of intent, decision-making supports: the questions "
                        "nobody else answers."),
                 path="/resources/life-planning", cta="Read the planning guide",
                 art_alt="Neighbors in the snowy village by an accessible van, a bus stop, and a covered table."),
        ],
        hope=dict(quote=HOPE_QUOTE, who=HOPE_WHO,
                  art_alt="Neighbors pinning notes of hope to a wall in the snowy village."),
        question=dict(
            q="How do we get through a big holiday gathering without everyone melting down?",
            short=("You cannot make a loud, crowded day calm. You can plan for the moment it gets to be too "
                   "much, for your child and for you."),
            steps=[
                ("Plan the exit before you go in.", "Know where the quiet room is, when you will leave, and "
                 "leave margin before and after. Pack the supports you both use, not only your child&rsquo;s."),
                ("Decide what matters ahead of time.", "Pick the one or two expectations that are essential and "
                 "let the rest wait. Two acceptable options beat inventing new ones mid-meltdown."),
                ("Set up a handoff.", "Agree on a phrase with another adult, like &ldquo;I am at yellow. Please "
                 "take over now.&rdquo; Needing a second grown-up is not failure."),
            ],
            links=[(f"{SITE}/resources/when-your-nervous-system-is-full", "Nervous system guide"),
                   (f"{SITE}/resources/sensory-processing", "Sensory processing")],
            disclaimer="Parent-to-parent guidance, not medical advice.",
        ),
        group_line="Thursdays, off Dec 24 and Dec 31",
        todo=[],
    ),
    # ------------------------------------------------------------------ January 2027
    dict(
        id="2027-01", send_on="2027-01-01", month="January", month_year="January 2027",
        subject="January: school dates + asking for an evaluation",
        preheader=("School dates as classes resume, a monthly respite morning, and a step-by-step answer "
                   "on asking your school for an evaluation."),
        hero_alt="Illustration of the village in winter: snowy homes, shops, and neighbors walking the path.",
        note=[
            ("Happy new year from Our Special Village. January is a month for fresh starts and paperwork, "
             "and this issue helps with both."),
            ("Inside: the school dates to know as classes start back, a step-by-step answer on asking your "
             "school for an evaluation, and a monthly respite morning for families who need a break."),
            ("At Village Hall on Saturday, January 9, Alyssa Engel of Cultivate Play talks DIR-Floortime, "
             "occupational therapy, neurodivergence, and PDA."),
            ("Whatever this year holds for your child, you do not have to figure it out alone."),
        ],
        note_highlight="you do not have to figure it out alone",
        chips=[("#deadlines", "School dates"), ("#question", "Asking for an evaluation"),
               ("#events", "Respite + events"), ("#library", "School guides")],
        three_things=[], all_deadlines=[], confirmed="", deadlines_meta="",
        village_hall=dict(
            VH_TBD,
            date="Saturday, January 9, 2027",
            time=VH_TIME,
            topic="DIR-Floortime, occupational therapy, neurodivergence, and PDA",
            guests=[dict(
                name="Alyssa Engel",
                role="Cultivate Play",
                photo=None,
                photo_alt="Alyssa Engel.",
                bio=ph("Alyssa&rsquo;s credentials, photo, and a short bio."),
            )],
        ),
        events=dict(
            featured=dict(
                title="rEcess &middot; Otter Creek Church and 99 Balloons",
                meta="Sat Jan 2 &middot; 8:00&ndash;11:45 AM &middot; Brentwood &middot; About 40 min",
                blurb=("A monthly respite morning: kids with disabilities and their siblings enjoy games and "
                       "activities while parents rest, run errands, or do whatever they need."),
                link=RECESS_LINK,
                art_alt="Neighbors gathered under a snowy pavilion, one in a wheelchair, with children nearby.",
            ),
            list=[],
            calendar_label="View the full January events calendar",
        ),
        library_title="From the library",
        guides=[
            dict(label="School", title="IEPs, 504s, and how to get one",
                 blurb=("The Tennessee timelines, your rights, a sample SAT meeting request, and the free "
                        "advocates who&rsquo;ll walk in with you."),
                 path="/resources/iep-504",
                 art_alt="A snowy school and a covered table where a parent meets with a teacher."),
            dict(label="Paying for care", title="The DDA Family Support Program",
                 blurb=("Up to $6,000 a year from Tennessee&rsquo;s Department of Disability and Aging for respite, "
                        "equipment, and home modifications."),
                 path="/resources/funding/family-support", cta="Read the Family Support guide",
                 art_alt="A family crossing a snowy stone footbridge toward a brick office building."),
        ],
        hope=dict(quote=HOPE_QUOTE, who=HOPE_WHO,
                  art_alt="Neighbors pinning notes of hope to a wall in the snowy village."),
        question=dict(
            q="How do I ask my child&rsquo;s school for a special education evaluation?",
            short=("Schools rarely offer first. You have to ask, in writing, and you can do it any time "
                   "of the school year."),
            steps=[
                ("Put the request in writing.", "Email the principal and copy the district special education "
                 "office. Describe what you see and ask for a full initial evaluation. Our guide has a letter to copy."),
                ("Know the two answers.", "The district must propose an assessment plan or refuse in writing "
                 "(Prior Written Notice). &ldquo;Let&rsquo;s try interventions first&rdquo; is not one of them."),
                ("Track the clock.", "Your signed consent starts 60 calendar days to evaluate and decide "
                 "eligibility. Put the dates in your phone; STEP TN can help: " + "{STEP}" + "."),
            ],
            links=[(f"{SITE}/resources/iep-504", "IEP &amp; 504 guide and letter"),
                   (f"{SITE}/resources/getting-evaluated", "Getting evaluated")],
            disclaimer="Parent-to-parent guidance, not legal advice.",
        ),
        group_line="Drop in any Thursday",
        todo=[],
    ),
    # ------------------------------------------------------------------ February 2027
    dict(
        id="2027-02", send_on="2027-02-01", month="February", month_year="February 2027",
        subject="February: school days off + finding a good therapist",
        preheader=("School days off, winter outings, guides on sensory processing and home safety, and how "
                   "to tell if a therapist is a good fit."),
        hero_alt="Illustration of the village in winter: snowy homes, shops, and neighbors walking the path.",
        note=[
            ("February is short and cold, and often long on indoor days. This issue gathers a few ways to "
             "get out of the house and two guides for the in-between times."),
            ("Our guides explain sensory processing in plain language and how to build a layered safety plan "
             "when childproofing is not enough. If you are looking for a new therapist, this month&rsquo;s "
             "question walks through what a good fit looks like."),
            ("Thank you for being part of this Village. It keeps growing because families like yours pass it along."),
        ],
        note_highlight="families like yours pass it along",
        chips=[("#deadlines", "School days off"), ("#events", "Winter outings"),
               ("#library", "Sensory + safety guides"), ("#question", "Finding a good therapist")],
        three_things=[], all_deadlines=[], confirmed="", deadlines_meta="",
        village_hall=dict(VH_TBD, date="Saturday, February 13, 2027", time=VH_TIME),
        events=dict(
            featured=dict(
                title="rEcess &middot; Otter Creek Church and 99 Balloons",
                meta="Sat Feb 6 &middot; 8:00&ndash;11:45 AM &middot; Brentwood &middot; About 40 min",
                blurb=("A monthly respite morning: kids with disabilities and their siblings enjoy games and "
                       "activities while parents rest, run errands, or do whatever they need."),
                link=RECESS_LINK,
                art_alt="Neighbors building and planting together in the snowy village.",
            ),
            list=[],
            calendar_label="View the full February events calendar",
        ),
        library_title="From the library",
        guides=[
            dict(label="Sensory", title="Sensory processing, explained",
                 blurb="All eight senses in plain language, and how to meet the need instead of fighting the behavior.",
                 path="/resources/sensory-processing",
                 art_alt="A snowy therapy clinic and porch where a child plays with sensory tools beside an adult."),
            dict(label="Safety", title="When childproofing isn&rsquo;t enough",
                 blurb=("A layered home-safety plan for children who open, climb over, copy, or dismantle "
                        "ordinary safeguards."),
                 path="/resources/safety-elopement", cta="Read the safety guide",
                 art_alt="A family at a snowy home with a ramp and an accessible van."),
        ],
        hope=dict(quote=HOPE_QUOTE, who=HOPE_WHO,
                  art_alt="Neighbors pinning notes of hope to a wall in the snowy village."),
        question=dict(
            q="How do I know if my child&rsquo;s therapist is a good fit?",
            short=("Fit matters more than a long list of initials. A good match can explain what they are "
                   "doing and why, and progress shows up outside the therapy room."),
            steps=[
                ("Ask what they do every week.", "What share of their caseload has needs like your child&rsquo;s, "
                 "and when do they refer out? Credentials are clues, not proof."),
                ("Watch how your child is treated.", "Green flags: your child&rsquo;s communication, including AAC "
                 "and &ldquo;no,&rdquo; is respected, and goals connect to real life."),
                ("Know you can switch.", "Repeated distress, loss of trust, or goals you did not agree to are valid "
                 "reasons to ask for a plan review, a different clinician, or a second opinion."),
            ],
            links=[(f"{SITE}/resources/choosing-a-therapist", "Choosing the right therapist"),
                   (f"{SITE}/resources/therapy-styles", "Therapy styles")],
            disclaimer="Parent-to-parent guidance, not medical advice.",
        ),
        group_line="Drop in any Thursday",
        todo=[],
    ),
]

# ---------------------------------------------------------------------------- dated items
# Verified Sept 28, 2026 against the official pages in research-notes-nov-2026-feb-2027.md.

RCS = ("https://www.rcschools.net/o/rcs/page/rcs-academic-calendars", "Rutherford County Schools calendar")
MCS = ("https://www.cityschools.net/calendar", "Murfreesboro City Schools calendar")
HC = ("https://www.healthcare.gov/quick-guide/dates-and-deadlines/", "HealthCare.gov dates")
MEDICARE = ("https://www.medicare.gov/health-drug-plans/open-enrollment", "Medicare.gov")
ACT_DATES = "https://www.act.org/content/act/en/products-and-services/the-act/registration/test-dates.html"
ACT_ACC = "https://www.act.org/content/act/en/products-and-services/the-act/registration/accommodations.html"
EFS = "https://www.tn.gov/education/efs.html"
IEA = "https://www.tn.gov/education/iea.html"
NIST = "https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst"
CONFIRMED = "Dates confirmed Sept 28. If something changed, reply and we will fix it."


def L(href, label):
    return f'<a href="{href}">{label}</a>'


RCS_MCS = f"{L(*RCS)} {L(*MCS)}"

# Disability grants and programs, verified Sept 28, 2026 (sources in research-notes-nov-2026-feb-2027.md).
FIRST_HAND = ("https://firsthandfoundation.org/grants/", "First Hand grants")
UHCCF = ("https://www.uhccf.org/apply-for-a-grant/", "UHCCF grants")
TTAP = ("https://www.tn.gov/humanservices/ds/ttap.html", "TTAP")
OAR = ("https://researchautism.org/self-advocates/postsecondary-scholarships/", "OAR scholarships")
MOSS = ("https://www.mossfoundation.org/scholarships/", "Moss scholarship")
STEP_UP = ("https://www.collegefortn.org/tennessee-step-up-scholarship/", "STEP UP")
SOTN = ("https://www.specialolympicstn.org/winter", "Special Olympics TN")
EASTERSEALS = ("https://tn.easterseals.com/get-support/areas-of-support/recreational-camp/adult-recreational-camp", "Easterseals camp")
UCP = ("https://www.ucpmidtn.org/family-support/", "UCP Family Support")


def first_hand(mon, day, wk):
    return (wk, day, mon, f"First Hand Foundation grant deadline: {mon}&nbsp;{day}",
            "For kids 18 and under with a medical need, within income limits. Pays for future therapy, equipment, "
            f"AAC and travel for care. Due the 15th of every month. {L(*FIRST_HAND)}")


def first_hand_thing(chip, date_words):
    return dict(chip=chip, items=[dict(
        title=f"First Hand Foundation grants: next deadline {date_words}",
        body=("Grants for kids 18 and under with a medical need, within income limits (for example $65,000 with "
              "one child). They pay for future therapy, equipment, AAC, and travel for care. Due the 15th of "
              "every month."),
        links=[FIRST_HAND])])


ALWAYS_OPEN = [
    ("Any", "-", "time", "UnitedHealthcare Children&rsquo;s Foundation grants",
     f"Up to $5,000 a year for kids 16 and under with commercial insurance. Reviewed monthly. {L(*UHCCF)}"),
    ("Any", "-", "time", "TTAP: try, borrow, or get help paying for assistive technology",
     f"Tennessee&rsquo;s free program for device demos, loans, and reused equipment. {L(*TTAP)}"),
]
KB_ROW = ("Any", "-", "time", "Katie Beckett (TennCare)",
          f'Apply any time; Part B has a waiting list. {L(SITE + "/resources/katie-beckett", "Katie Beckett guide")}')

NOV, DEC, JAN, FEB = ISSUES

NOV.update(
    confirmed=CONFIRMED,
    deadlines_meta="Dates confirmed Sept 28, 2026. Teen, college, and insurance items live here so the email can stay short.",
    three_things=[
        first_hand_thing(("Sun", "15", "Nov"), "Sun Nov 15"),
        dict(chip=("Tue", "3", "Nov"), items=[dict(
            title="No school Tue Nov 3 and Thanksgiving week, Nov 23 to 27",
            body=("Both Rutherford County Schools and Murfreesboro City Schools. Progress reports and report "
                  "cards come home the first week of November; ask for IEP progress data."),
            links=[RCS, MCS])]),
        dict(chip=("Nov", "1", "Jan 15"), items=[dict(
            title="HealthCare.gov open enrollment: Nov 1 to Jan 15",
            body=("Shop or renew a 2027 Marketplace plan. Enroll by Dec 15 for coverage that starts Jan 1. "
                  "Kids may qualify for TennCare or CoverKids any time."),
            links=[HC])]),
    ],
    all_deadlines=[
        ("Grants and help", [first_hand("Nov", "15", "Sun")] + ALWAYS_OPEN),
        ("School and community", [
            ("Tue", "3", "Nov", "Election Day: no school for students",
             f"Rutherford County Schools teacher admin day; Murfreesboro City Schools parent-teacher conferences and report cards. {RCS_MCS}"),
            ("Wed", "4", "Nov 6", "Rutherford County Schools progress reports: Nov&nbsp;4&ndash;6", L(*RCS)),
            ("Mon", "23", "Nov 27", "Thanksgiving break: Nov&nbsp;23&ndash;27",
             f"Students out all week in both districts. {RCS_MCS}"),
        ]),
        ("Insurance and health", [
            ("Nov", "1", "Jan 15", "HealthCare.gov: Nov&nbsp;1&ndash;Jan&nbsp;15",
             f"Enroll by Dec 15 for Jan 1 coverage. {L(*HC)}"),
            ("Oct", "15", "Dec 7", "Medicare open enrollment ends Dec&nbsp;7",
             f"For grandparents and caregivers on Medicare. TN SHIP: 1-877-801-0044. {L(*MEDICARE)}"),
            KB_ROW,
        ]),
        ("Teens and college", [
            ("Mon", "2", "Nov", "Tennessee Promise application: Mon&nbsp;Nov&nbsp;2",
             'Class of 2027. <a href="https://www.tn.gov/thec/news/2026/9/2/college-application.html">THEC</a>'),
            ("Fri", "6", "Nov", "ACT Dec&nbsp;12: registration and accommodations by Fri&nbsp;Nov&nbsp;6",
             f'Accommodations go through your school testing coordinator. Late registration ends Nov 29. {L(ACT_ACC, "ACT accommodations")}'),
        ]),
    ],
)

DEC.update(
    confirmed=CONFIRMED,
    deadlines_meta="Dates confirmed Sept 28, 2026. Teen, college, and insurance items live here so the email can stay short.",
    three_things=[
        dict(chip=("Fri", "18", "Dec"), items=[dict(
            title="Winter break: last day Fri Dec 18, back Tue Jan 5",
            body=("Dec 18 is a short day in Rutherford County and Murfreesboro City Schools. Break runs Dec 21 to Jan 1, and Mon Jan 4 is also "
                  "no school for students. A visual countdown can make the change in routine easier."),
            links=[RCS, MCS])]),
        dict(chip=("Tue", "15", "Dec"), items=[dict(
            title="HealthCare.gov: pick a plan by Tue Dec 15 for Jan 1",
            body="Open enrollment runs to Jan 15, but plans chosen after Dec 15 start Feb 1.",
            links=[HC])]),
        first_hand_thing(("Tue", "15", "Dec"), "Tue Dec 15"),
    ],
    all_deadlines=[
        ("School", [
            ("Fri", "18", "Dec", "Short day, last day before winter break",
             f"Rutherford County Schools 2-hour day ends the 2nd nine weeks; Murfreesboro City Schools half day. {RCS_MCS}"),
            ("Mon", "21", "Jan 1", "Winter break: Dec&nbsp;21&ndash;Jan&nbsp;1", RCS_MCS),
            ("Mon", "4", "Jan", "In-service day: no school for students", RCS_MCS),
            ("Tue", "5", "Jan", "Students return", RCS_MCS),
        ]),
        ("Insurance and health", [
            ("Mon", "7", "Dec", "Medicare open enrollment ends", f"TN SHIP: 1-877-801-0044. {L(*MEDICARE)}"),
            ("Tue", "15", "Dec", "HealthCare.gov: last day for Jan&nbsp;1 coverage", L(*HC)),
            ("Fri", "15", "Jan", "HealthCare.gov open enrollment ends", L(*HC)),
            KB_ROW,
        ]),
        ("Grants and help", [
            first_hand("Dec", "15", "Tue"),
            ("Fri", "4", "Dec 6", "Easterseals Tennessee adult weekend camp: Dec&nbsp;4&ndash;6",
             f"For adults 17 and up with disabilities; $725. {L(*EASTERSEALS)}"),
        ] + ALWAYS_OPEN),
        ("Money and benefits", [
            ("Any", "-", "time", "ABLE TN: up to $20,000 in contributions per calendar year",
             'Working beneficiaries may be able to add more through ABLE to Work. '
             '<a href="https://able.treasury.tn.gov/faqs">ABLE TN FAQs</a>'),
        ]),
        ("Teens and college", [
            ("Thu", "10", "Dec", "EFS family office hours, 10&ndash;11&nbsp;AM&nbsp;CT",
             f'For current Education Freedom Scholarship families. 2027&ndash;28 application dates not posted yet. {L(EFS, "EFS")}'),
            ("Sat", "12", "Dec", "ACT test date", f'Scores out Tue Dec 22. {L(ACT_DATES, "ACT dates")}'),
            ("Dec", "", "Apr", "OAR college scholarships open in December",
             f"$3,000 for autistic students starting college, trade, vocational, or life-skills programs. Due in April. {L(*OAR)}"),
        ]),
    ],
)

JAN.update(
    confirmed=CONFIRMED,
    deadlines_meta="Dates confirmed Sept 28, 2026. Teen, college, and benefits items live here so the email can stay short.",
    three_things=[
        dict(chip=("Tue", "5", "Jan"), items=[dict(
            title="Back to school Tue Jan 5 (no school Mon Jan 4)",
            body=("Report cards come home Wed Jan 6 (Murfreesboro City Schools) and Fri Jan 8 (Rutherford County Schools). A good time to ask how IEP goals "
                  "are tracking before spring."),
            links=[RCS, MCS])]),
        dict(chip=("Fri", "15", "Jan"), items=[dict(
            title="Last day of HealthCare.gov open enrollment: Fri Jan 15",
            body="Plans chosen Dec 16 to Jan 15 start Feb 1.",
            links=[HC])]),
        dict(chip=("Jan", "1", "Apply"), items=[dict(
            title="Family Support funds: apply early in the year",
            body=("Tennessee&rsquo;s Family Support Program gives flexible money for respite, equipment, camp, and "
                  "home changes to people with severe disabilities who are not on a waiver. Funds run out, so ask "
                  "UCP of Middle Tennessee (615-796-3341) for this year&rsquo;s dates."),
            links=[UCP, (SITE + "/resources/funding/family-support", "Family Support guide")])]),
    ],
    all_deadlines=[
        ("School and community", [
            ("Mon", "4", "Jan", "In-service day: no school for students", RCS_MCS),
            ("Tue", "5", "Jan", "Students return", RCS_MCS),
            ("Wed", "6", "Jan", "Murfreesboro City Schools report cards", L(*MCS)),
            ("Fri", "8", "Jan", "Rutherford County Schools report cards, 2nd nine weeks", L(*RCS)),
            ("Tue", "12", "Jan", "Tennessee General Assembly convenes",
             'The legislature meets on the second Tuesday of January in odd years. '
             '<a href="https://sos.tn.gov/civics/guides/legislative-branch">TN Secretary of State</a>'),
            ("Mon", "18", "Jan", "MLK Day: no school", RCS_MCS),
        ]),
        ("Insurance and health", [
            ("Fri", "15", "Jan", "HealthCare.gov open enrollment ends", L(*HC)),
            KB_ROW,
        ]),
        ("Money and benefits", [
            ("Jan", "1", "Apply", "Family Support Program: apply early in the year",
             f'Up to $6,000 a year for respite, equipment, and home changes. Other regions open Jan&nbsp;1; confirm '
             f'Rutherford&rsquo;s dates with UCP of Middle Tennessee (615-796-3341). {L(*UCP)}'),
            ("Fri", "15", "Jan", "EFS: projected quarter 3 payment", f'For current Education Freedom Scholarship families. {L(EFS, "EFS")}'),
        ]),
        ("Grants and help", [
            first_hand("Jan", "15", "Fri"),
            ("Sun", "24", "Jan 26", "Special Olympics Tennessee Winter Games: Jan&nbsp;24&ndash;26", f"Gatlinburg. {L(*SOTN)}"),
        ] + ALWAYS_OPEN),
        ("Teens and college", [
            ("Thu", "14", "Jan", "EFS family office hours, 1&ndash;2&nbsp;PM&nbsp;CT", L(EFS, "EFS")),
            ("Fri", "22", "Jan", "ACT Feb&nbsp;27: registration and accommodations by Fri&nbsp;Jan&nbsp;22",
             f'Through your school testing coordinator. Late registration ends Feb 9. {L(ACT_ACC, "ACT accommodations")}'),
            ("Jan", "1", "Mar 31", "P. Buckley Moss Scholarship: Jan&nbsp;1&ndash;Mar&nbsp;31",
             f"Up to $1,000 a year for a graduating senior with learning differences heading into visual arts. {L(*MOSS)}"),
        ]),
    ],
)

FEB.update(
    confirmed=CONFIRMED,
    deadlines_meta="Dates confirmed Sept 28, 2026. Teen, college, and school-choice items live here so the email can stay short.",
    three_things=[
        first_hand_thing(("Mon", "15", "Feb"), "Mon Feb 15"),
        dict(chip=("Tue", "16", "Feb"), items=[dict(
            title="IEA applications projected to open Tue Feb 16",
            body=("Tennessee&rsquo;s Individualized Education Account for 2027&ndash;28 needs an active IEP and a "
                  "prior year in a Tennessee public school."),
            links=[(IEA, "IEA")])]),
        dict(chip=("Thu", "11", "Mar"), items=[dict(
            title="Looking ahead: no school Thu Mar 11, clocks spring forward Sun Mar 14",
            body=("Rutherford County and Murfreesboro City Schools are out Mar 11. If sleep is fragile, shift bedtime 10 to 15 minutes a night "
                  "the week before the time change."),
            links=[RCS, MCS, (NIST, "How DST works")])]),
    ],
    all_deadlines=[
        ("Grants and help", [
            first_hand("Feb", "15", "Mon"),
            ("Mon", "1", "Mar", "Tennessee STEP UP Scholarship: spring deadline Mar&nbsp;1",
             f"For students with intellectual disabilities in inclusive college programs. Up to $2,850 a semester. {L(*STEP_UP)}"),
        ] + ALWAYS_OPEN),
        ("School and community", [
            ("Wed", "3", "Feb 5", "Rutherford County Schools progress reports: Feb&nbsp;3&ndash;5", L(*RCS)),
            ("Fri", "12", "Feb", "Murfreesboro City Schools planning day: no school for city students", L(*MCS)),
            ("Mon", "15", "Feb", "Presidents&rsquo; Day: no school", RCS_MCS),
            ("Thu", "11", "Mar", "No school for students", f"Rutherford County Schools admin day; Murfreesboro City Schools parent-teacher conferences. {RCS_MCS}"),
            ("Sun", "14", "Mar", "Clocks spring forward", f'Daylight saving time begins at 2:00 AM. {L(NIST, "NIST")}'),
            ("Mon", "29", "Apr 2", "Spring break: Mar&nbsp;29&ndash;Apr&nbsp;2", RCS_MCS),
        ]),
        ("School choice", [
            ("Tue", "16", "Feb", "IEA 2027&ndash;28: projected to open",
             f'No closing date posted yet; last year&rsquo;s window ran Feb 17 to Apr 17. {L(IEA, "IEA")}'),
        ]),
        ("Insurance and health", [KB_ROW]),
        ("Teens and college", [
            ("Tue", "9", "Feb", "ACT Feb&nbsp;27: late registration ends", L(ACT_DATES, "ACT dates")),
            ("Sat", "27", "Feb", "ACT test date", f'Accommodated testing window Feb 27 to Mar 7. {L(ACT_ACC, "ACT accommodations")}'),
        ]),
    ],
)

# ---------------------------------------------------------------------------- Discovery Center
# Verified Sept 28, 2026 on https://explorethedc.org/series/all-access-nights/ (not yet in events.json).
DC_URL = "https://explorethedc.org/series/all-access-nights/"

NOV["events"]["featured"] = dict(
    title="All Access Night: Fall on the Farm &middot; Discovery Center",
    meta="Thu Nov 12 &middot; 6:00&ndash;8:00 PM &middot; Murfreesboro &middot; Free, registration required",
    blurb="Smaller crowds and reduced sensory input for families of children with special needs.",
    link=(DC_URL, "Reserve your spot"),
    # Real photo from the Discovery Center's own site (their homepage share image). Their site has no
    # Fall on the Farm photo, and this environment can't download from explorethedc.org, so it is linked.
    photo_url="https://www.explorethedc.org/wp-content/uploads/2024/03/Discovery-Center.jpg",
    art_alt="The Discovery Center at Murfree Spring in Murfreesboro.",
)
NOV["events"]["list"] = [
    dict(chip=("Sat", "7", "Nov"), title="Sensory Sessions with Love Learning Music &middot; Linebaugh Library",
         meta=LINEBAUGH_META, link=LINEBAUGH_LINK),
    dict(chip=("Sat", "7", "Nov"), title="rEcess &middot; Otter Creek Church and 99 Balloons",
         meta=RECESS_META, link=RECESS_LINK),
    dict(chip=("Sat", "7", "Nov"), title="Game Day &middot; Autism Tennessee", meta=GAME_DAY_META, link=GAME_DAY_LINK),
] + [e for e in NOV["events"]["list"] if e["chip"][1] in ("15", "21")]

DEC["events"]["list"].insert(3, dict(
    chip=("Thu", "10", "Dec"), title="All Access Night: Holiday Party &middot; Discovery Center",
    meta="6:00&ndash;8:00 PM &middot; Murfreesboro &middot; Free, registration required &middot; Smaller crowds, less sensory input",
    link=(DC_URL, "Reserve your spot")))

WINTER_NOTE = ("Winter calendars are still filling in. We add events as organizers post them, so check the "
               "full calendar before your weekend.")
for _i in (JAN, FEB):
    _i["events"]["note"] = WINTER_NOTE

# ---------------------------------------------------------------------------- still to do (shown on the preview page)
COMMON_TODO = [
    "Wall of Hope: add one parent story (two to four sentences) and the parent&rsquo;s first name. It signs off as their name, then Murfreesboro.",
    "Village Hall: add the date, time, topic, guest name, role, photo, and a short bio.",
    "My draft of your welcome note: edit it so it sounds like you.",
]
NOV["todo"] = [
    COMMON_TODO[0],
    "Kerry Hankins-Grider: add her bio and a photo (Village Hall card), and one or two intro sentences in your note.",
    "Amanda&rsquo;s role line says &ldquo;LAMP Certified Professional &middot; PRC-Saltillo&rdquo;. Add her job title if she has one.",
    "Registration: the site still says Nov 14 registration is not open. Open it before Nov 1.",
    "Fall on the Farm photo: the Discovery Center site has no event photo, so this uses their building photo "
    "(it shows in inboxes; the preview shows your painting instead). Send a picture you like to swap it.",
    "More sensory Santa, library, and theater dates usually post in October, so they are worth a re-check mid-October.",
]
DEC["todo"] = [
    COMMON_TODO[0],
    "Village Hall: Katie Dell of Behavior Cubed, Sat Dec 12, all things behavior. Add her credentials, photo, and a short bio.",
    COMMON_TODO[2],
]
JAN["todo"] = [
    COMMON_TODO[0],
    "Village Hall: Alyssa Engel of Cultivate Play, Sat Jan 9. Add her credentials, photo, and a short bio.",
    COMMON_TODO[2],
    "Only one January event is confirmed so far (rEcess, Jan 2). Discovery Center, Autism Tennessee and "
    "ABLE Youth had not posted January dates on Sept 28; I will add them when they do."]
FEB["todo"] = [
    COMMON_TODO[0],
    "Village Hall, Sat Feb 13: Bradi (Braxy Speech) may be the guest, waiting on confirmation. Then add her name, role, photo, bio, and topic.",
    COMMON_TODO[2],
] + [
    "Only one February event is confirmed so far (rEcess, Feb 6). Same organizers to re-check in January."]

# Keep November under Gmail's ~102 KB clip once the Wall of Hope story is added.
NOV["events"]["list"] = [e for e in NOV["events"]["list"] if e["chip"][1] != "16"]


# Taylor (Sept 28): less school-heavy. Grants and help lead every deadlines page.
for _i in ISSUES:
    _i["all_deadlines"].sort(key=lambda sec: sec[0] != "Grants and help")
NOV["events"]["list"].sort(key=lambda e: int(e["chip"][1]))
