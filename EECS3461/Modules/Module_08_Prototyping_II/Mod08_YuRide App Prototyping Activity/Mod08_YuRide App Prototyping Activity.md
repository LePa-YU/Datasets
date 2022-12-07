### Mod08: YuRide App Prototyping Activity Specification

**Format**: group based (see ==Module 08 Teams==, which will be the same as ==Module 06 Teams (Finalized)==, unless the course instructors have modified the groups) 

**Weight:** 5% 

==highlighted phrases== indicate places which are links to other documents (links will become active within 24 hours of this document's release)

**Objectives**

- to gain further experience in analysing journey maps to prototyping
- to gain further experience in prototyping mobile apps
- to develop skills in the real-life application of theoretical concepts from  ==R-Design-III== 
- to apply domain knowledge gained from Mod06: Journey Mapping Activity

#### Instructions

1. read through the activity description
2. read the activity expectations: deliverables and grading expectations
3. then (AND ONLY THEN) begin the activity

#### Activity Description

You have been provided with a partially-implemented prototype in Figma for the app called "YURide"

You are provided with the YURide business plan, which provides the background on the goals of the app and its design. Of particular relevance:

- p. 51, Consumer Journey
- p. 9, Driver Journey
- p. 10, Customer Journey

A few notes:

- The business plan provisions for payment post-ride, where ride-sharers pay for their ride using their YUCard. The prototype implements a strategy whereby ride-sharers purchase points in advance, and then use the points to pre-pay for rides.  YURide has permission from the university to use YUCard as a payment card, but there are some delays.  So the plan is to use pre-payment for the initial launch, and then shift to post-payment using YUCard later.
- The prototype focuses on campus-inbound trips only.  
- The prototype is designed as follows: 
  - the passenger puts the target approx arrival time under 'Settings' (under the assumption that people generally have fixed schedules)
  - the passenger enters the source destination under a special-purpose screen.

#### Task

Take the Customer Journey and the Figma prototype as a starting point.

Your team will need to build/improve functionality around the 'request' scenario: a ride-sharer who requests a one-time ride to campus to arrive at a specific time and to be picked up at a specific location.  

There are many other use scenarios, such as repeated, recurring ride-shares.  There is also the driver view. We are not covering these scenarios in this activity. 

Your task is to create a prototype for this specific scenario.   In completing this activity, your team may notice certain issues arise.  Your team may optionally create additional functionality in the prototype to address these issues.  This would be considered going above and beyond the requirements of the acivity.  As well, team members may use ideas generated as the basis for the Mod09:  YURide Design Extension Activity (optional). 

Modify the Figma prototype in order to create a full walkthrough of the following Passenger Scenario.

---

#### Passenger Scenario:

This scenario is a fleshed-out version of "Customer Journey"

The scenario begins after the customer has downloaded the app

1. User logs in (assume it is Wednesday at 4:00pm)
2. User checks their own settings, verifies that they have 0 points
3. User authenticates as a rider
4. User indicates they want to arrive on campus on Friday at 10am, they are coming from the following address: 25 Bloomsbury Ave, Brampton, Ontario (this address was randomly chosen and is not meant to indicate anyone's address)  
5. The cost of the ride is 125 points, and the user does not have enough points.
6. User selects option to purchase more points.
7. User purchases 500 points.
8. Users returns to set up screen, specifies target arrival time on campus, specifies desired pick-up location
8. User submits requests and receives feedback that request processing is in progress.
8. User received notification of successful match with driver and notification of pick up time.
8. User is successfully picked up and driven to campus
8. User is presented with option to provide driver feedback. 

---

#### Deliverable #1: Figma File

- Select the option under File -> Save local copy..

  save the file locally `Mod08_SecY_GroupZZ_Figma.fig`

- submit this *.fig file under the submission module ==Mod08: YURide App Prototyping Activity==



---

#### Expectations

The submissions will be assessed using the 4-point scale (Below expectations, Marginally meets expectations, Meets expectations, Exceeds expectations), except where noted otherwise.

To meet expectations:

1. The submission adheres to the specification (e.g., file name and file format are correct, etc) *this is a binary assessment, yes/no*
2. Completeness: all specified steps in the scenario are included in the prototype (weight: 2)
3. Flows: prototype allows user to move smoothly from each scenario step to the next using intuitive input actions
4. Screen Design and Layout: components on the screen adhere to design principles: *visibility*, *constraints*, *consistency*, *feedback*; flows implement strategies that demonstrate understanding of the gulf of execution and gulf of evaluation
5. Problem-Solving: the prototype demonstrates solutions to issues that arise; considerations not covered under the scenario
