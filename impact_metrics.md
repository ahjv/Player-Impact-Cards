\# 📊 Player Impact Metrics



\## 🔹 DIS (Defensive Impact Score)



\*\*Definition\*\*:

Quantifies a player's impact on team defense by measuring how much the team improves defensively while they’re on the court.



\*\*Formula (Conceptual)\*\*:

Let `D\\\_on` = team defensive rating when player is on court

Let `D\\\_off` = team defensive rating when player is off court

Then:

DIS\_raw = D\_off - D\_on



\*\*Interpretation\*\*:

Higher values = more defensive suppression



\*\*Normalization Strategy\*\*:

DIS = 100 + (DIS\_raw - league\_avg\_DIS\_raw) / std\_DIS\_raw \* 10



\*\*Data Needed\*\*:

\- On/off team defensive rating per player per game (via nba\_api)



---



\## 🔹 OGI (Offensive Gravity Index)



\*\*Definition\*\*:

Measures how much a player draws defenders and creates scoring opportunities through passing and movement.



\*\*Formula (Conceptual)\*\*:

Let A = assists

Let S = 3PA (three-point attempts)

Then:

OGI\_raw = A + 0.5 \* S



\*\*Normalization Strategy\*\*:

Z-score scaling or percentile binning



\*\*Data Needed\*\*:

\- Assists and 3PA from box scores

\- Optional: screen assists, usage rate (if available)



---



\## 🔹 Contest Rate



\*\*Definition\*\*:

Measures how frequently a player contests shots on defense.



\*\*Formula (Practical)\*\*:

ContestRate = (Blocks + Steals) / Minutes \* 36



\*\*Interpretation\*\*:

Higher value = more shot disruption



\*\*Data Needed\*\*:

\- STL, BLK, MIN from box score

\- Optional: contest stats if available



---



\## 🔹 Rim Deterrence Score



\*\*Definition\*\*:

Measures how much a player reduces opponent paint attempts when they’re on the floor.



\*\*Formula (Conceptual)\*\*:

RimDeterrence = OppPaintFGA\_off - OppPaintFGA\_on



\*\*Interpretation\*\*:

Higher = opponents avoid attacking the rim when this player is on



\*\*Data Needed\*\*:

\- Opponent paint stats with player on/off court



---



\## 🔹 TO Pressure (Turnover Pressure)



\*\*Definition\*\*:

Captures how much a defender forces turnovers through active pressure.



\*\*Formula (Practical)\*\*:

TO\_Pressure = (Steals) / Minutes \* 36



\*\*Interpretation\*\*:

> 2.0 = disruptive  

> 3.5+ = elite pressure



\*\*Data Needed\*\*:

\- Steals and minutes from box score

\- Optional: deflections if available



---



\## 🔹 On/Off Net Rating Swing



\*\*Definition\*\*:

Measures how much a player improves overall team performance across both ends of the court.



\*\*Formula\*\*:

NetRating\_on = OffRtg\_on - DefRtg\_on

NetRating\_off = OffRtg\_off - DefRtg\_off

OnOffSwing = NetRating\_on - NetRating\_off



\*\*Interpretation\*\*:

Positive = team is better with player on the court



\*\*Data Needed\*\*:

\- On/Off Offensive \& Defensive Ratings

