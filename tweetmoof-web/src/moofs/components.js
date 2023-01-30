import React, { useState, useEffect } from "react";
import { MoofsList } from "./list";
import { MoofCreate } from "./create";
import { Moof } from "./detail";
import { apiMoofDetail } from "./lookup";
import { FeedList } from "./feed";

export function FeedComponent(props) {
  const [newMoofs, setNewMoofs] = useState([]);
  const canMoof = props.canMoof === "false" ? false : true;
  const handleNewMoof = (newMoof) => {
    let tempNewMoofs = [...newMoofs];
    tempNewMoofs.unshift(newMoof);
    setNewMoofs(tempNewMoofs);
  };

  return (
    <div className={props.className}>
      {canMoof === true && (
        <MoofCreate didMoof={handleNewMoof} className="col-12 mb-3" />
      )}
      <FeedList newMoofs={newMoofs} {...props} />
    </div>
  );
}

export function MoofsComponent(props) {
  const [newMoofs, setNewMoofs] = useState([]);
  const canMoof = props.canMoof === "false" ? false : true;
  const handleNewMoof = (newMoof) => {
    let tempNewMoofs = [...newMoofs];
    tempNewMoofs.unshift(newMoof);
    setNewMoofs(tempNewMoofs);
  };

  return (
    <div className={props.className}>
      {canMoof === true && (
        <MoofCreate didMoof={handleNewMoof} className="col-12 mb-3" />
      )}
      <MoofsList newMoofs={newMoofs} {...props} />
    </div>
  );
}

export function MoofDetailComponent(props) {
  const { moofId } = props;
  const [didLookup, setDidLookup] = useState(false);
  const [moof, setMoof] = useState(null);

  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setMoof(response);
    } else {
      alert("There was an error finding your moof.");
    }
  };

  useEffect(() => {
    if (didLookup === false) {
      apiMoofDetail(moofId, handleBackendLookup);
      setDidLookup(true);
    }
  }, [moofId, didLookup, setDidLookup]);
  return moof === null ? null : (
    //<React.StrictMode>
    <Moof moof={moof} className={props.className} />
    //</React.StrictMode>
  );
}
