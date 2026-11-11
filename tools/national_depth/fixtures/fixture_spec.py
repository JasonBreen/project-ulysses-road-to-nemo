"""A small, deliberately complete spec for compiler tests. Never shipped."""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='DOR', name='Dorondo', root='usea', package='fixture', themes=('rail', 'civil', 'industry'))
SOURCES = (Source('Provisional gameplay', 'Compiler test fixture; not shipped.'),)
LONG = ('The council met in the old customs hall, where the timetable boards still showed services that had not run for a decade. '
        'Delegates from the river towns asked for a plan that their own engineers could keep, not one that would need foreign crews.')
PARAGRAPHS = (LONG + ' The minutes record a long argument about who would pay for the first survey, and a shorter one about who would sign it.',
              LONG + ' The engineers asked for one season of measurements before anyone promised a date; the ministers asked for a date before anyone paid.',
              LONG + ' In the end the hall agreed to publish both the survey and its cost, so that the next council could see what had been bought and why.')
IDEAS = (IdeaDef('rail_board', 'Rail Board', 'A small board that keeps the rail survey honest.', {'production_speed_infrastructure_factor': 0.1}, ('rail', 'document')),
         IdeaDef('works_board', 'Works Board', 'A works office for the river towns.', {'production_speed_buildings_factor': 0.05}, ('tools', 'civil')))
EVENTS = (EventDef('survey', 'The Customs Hall Survey', PARAGRAPHS,
                   (Option('Publish the survey and its cost.', (Stability(0.02), Event('ledger', 30))), Option('Keep the cost in committee.', (PP(25),))), picture=1),
          EventDef('ledger', 'The Published Ledger', PARAGRAPHS,
                   (Option('Answer the questions in the hall.', (Stability(0.01),)), Option('Refer them to the engineers.', (PP(10),))), picture=2))
DECISIONS = (DecisionDef('river_dock', 'A Dock for the River Fleet', 'Build one dock on the coast once the gauge is agreed.', 50,
                         (Build('dockyard', 1, 409),), requires=(HasFlag('gauge_agreed'),)),
             DecisionDef('works_levy', 'A Works Levy', 'Raise a small levy for the works office; it can be repeated each year.', 25,
                         (PP(30),), cooldown=365))
OFFICES = (Office('council', 'River Towns Council', 'A collective council of the river towns.', 'democratic', 'centrism'),)
BRANCHES = (
    Branch('rail', 'The Rail Survey', 1991, 'FOCUS_FILTER_INDUSTRY', (
        Focus('rail_survey', 'Survey the River Line', 'Measure the line before promising it.', ('rail', 'document'), reward=(Idea('rail_board'),)),
        Focus('rail_gauge', 'One Gauge for the Valley', 'Agree one gauge.', ('rail', 'tools'), after=('rail_survey',), exclusive=('rail_spurs',),
              reward=(Build('infrastructure'), Flag('gauge_agreed'))),
        Focus('rail_spurs', 'Spurs to the Mines', 'Build spurs instead.', ('rail', 'industry'), after=('rail_survey',), reward=(Build('industrial_complex'),)),
        Focus('rail_timetable', 'A Published Timetable', 'Publish it.', ('document', 'rail'), after_any=('rail_gauge', 'rail_spurs'),
              requires=(HasFlag('gauge_agreed'),), reward=(Event('survey'),)),
    )),
    Branch('works', 'River Works', 1993, 'FOCUS_FILTER_STABILITY', (
        Focus('works_office', 'Open a Works Office', 'Open it.', ('tools', 'civil'), reward=(Idea('works_board'),)),
        Focus('works_council', 'The River Towns Council', 'Hand the works to a council.', ('assembly', 'civil'), after=('works_office',), cost=10,
              reward=(Regime('council'),)),
        Focus('works_research', 'Engineering Courses', 'Train engineers.', ('science', 'training'), after=('works_office',),
              reward=(Research('construction_tech'), Tooltip('Courses run at the works office.'))),
    )),
    Branch('later', 'The Later Years', 2004, 'FOCUS_FILTER_POLITICAL', (
        Focus('later_review', 'Review the Works', 'Look back.', ('scales', 'document'), reward=(SwapIdea('works_board', 'rail_board'), XP('army', 10)),
              requires=(NotGlobal('belka_won_belkan_war'),)),
    )),
    Branch('decade', 'The Second Decade', 2010, 'FOCUS_FILTER_INDUSTRY', (
        Focus('decade_yards', 'Yards on the Coast', 'Open yards.', ('navy', 'tools'), reward=(Build('dockyard', 1, 475),)),
    )),
)
