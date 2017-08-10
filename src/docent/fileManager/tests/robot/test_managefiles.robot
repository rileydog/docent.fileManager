# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s docent.fileManager -t test_managefiles.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src docent.fileManager.testing.DOCENT_FILEMANAGER_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_managefiles.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a managefiles
  Given a logged-in site administrator
    and an add managefiles form
   When I type 'My managefiles' into the title field
    and I submit the form
   Then a managefiles with the title 'My managefiles' has been created

Scenario: As a site administrator I can view a managefiles
  Given a logged-in site administrator
    and a managefiles 'My managefiles'
   When I go to the managefiles view
   Then I can see the managefiles title 'My managefiles'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add managefiles form
  Go To  ${PLONE_URL}/++add++managefiles

a managefiles 'My managefiles'
  Create content  type=managefiles  id=my-managefiles  title=My managefiles


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the managefiles view
  Go To  ${PLONE_URL}/my-managefiles
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a managefiles with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the managefiles title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
