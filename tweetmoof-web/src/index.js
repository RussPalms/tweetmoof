import React from "react";
//import {
//hydrateRoot,
//  createRoot,
//} from "react-dom/client";
import ReactDOM from "react-dom";
import "./index.css";
//import reportWebVitals from "./reportWebVitals";
import { ProfileBadgeComponent } from "./profiles";
import { FeedComponent, MoofsComponent, MoofDetailComponent } from "./moofs";

const e = React.createElement;
const moofsEl = document.getElementById("tweetmoof");
//const tweetmoof = createRoot(moofsEl);
////const tweetmoof = hydrateRoot(moofsEl, MoofsComponent);
if (moofsEl) {
  //tweetmoof.render(React.createElement(MoofsComponent, moofsEl.dataset));
  ReactDOM.render(e(MoofsComponent, moofsEl.dataset), moofsEl);
}

const moofFeedEl = document.getElementById("tweetmoof-feed");
if (moofFeedEl) {
  ReactDOM.render(e(FeedComponent, moofFeedEl.dataset), moofFeedEl);
  //createRoot(moofFeedEl).render(e(FeedComponent, moofFeedEl.dataset));
}

const moofDetailElements = document.querySelectorAll(".tweetmoof-detail");
moofDetailElements.forEach((container) => {
  //const moofRoot = hydrateRoot(container, MoofDetailComponent);
  //moofRoot.render(React.createElement(MoofDetailComponent, container.dataset));
  //try {
  //createRoot(container).render(
  //  React.createElement(MoofDetailComponent, container.dataset)
  //);
  //});

  //);
  //} catch (exceptionVar) {
  //console.log(exceptionVar);
  //} finally {
  ReactDOM.render(e(MoofDetailComponent, container.dataset), container);
  //}
});
//reportWebVitals();
//console.log("wtf");
//const userProfileBadgeElements = document.querySelectorAll(
//  ".tweetmoof-profile-badge"
//);
//console.log(userProfileBadgeElements);
//if (userProfileBadgeElements.length === 0) {
//  console.log("Something is fucked up . . .");
//}
//try {
//console.log(typeof userProfileBadgeElements);

//userProfileBadgeElements.forEach((container) => {
//  console.log("fuck");
//  ReactDOM.render(e(ProfileBadgeComponent, container.dataset), container);
//});

//} catch (e) {
//console.log("WHAT THE FUCK");
//}

const badgeEl = document.getElementById("tweetmoof-profile-badge");
if (badgeEl) {
  //  console.log(badgeEl);
  ReactDOM.render(e(ProfileBadgeComponent, badgeEl.dataset), badgeEl);
  //createRoot(badgeEl).render(e(ProfileBadgeComponent, badgeEl.dataset));
}
