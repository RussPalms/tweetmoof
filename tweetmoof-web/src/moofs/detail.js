import React, { useState } from "react";
import { ActionBtn } from "./buttons";
import { UserDisplay, UserPicture } from "../profiles";

export function ParentMoof(props) {
  const { moof } = props;
  return moof.parent ? (
    <Moof
      isRemoof
      remoofer={props.remoofer}
      hideActions
      className={" "}
      moof={moof.parent}
    />
  ) : null;
}

export function Moof(props) {
  const { moof, didRemoof, hideActions, isRemoof, remoofer } = props;
  const [actionMoof, setActionMoof] = useState(props.moof ? props.moof : null);
  let className = props.className ? props.className : "col-10 mx-auto col-md-6";
  className = isRemoof === true ? `${className} p-2 border rounded` : className;
  const path = window.location.pathname;
  const match = path.match(/(?<moofid>\d+)/);
  const urlMoofId = match ? match.groups.moofid : -1;
  const isDetail = `${moof.id}` === `${urlMoofId}`;

  const handleLink = (event) => {
    event.preventDefault();
    window.location.href = `/${moof.id}`;
  };

  const handlePerformAction = (newActionMoof, status) => {
    if (status === 200) {
      setActionMoof(newActionMoof);
    } else if (status === 201) {
      // let the moof list know
      if (didRemoof) {
        //console.log(newActionMoof);
        didRemoof(newActionMoof);
      }
    }
  };

  return (
    <div className={className}>
      {isRemoof === true && (
        <div className="mb-2">
          <span className="small text-muted">
            Remoof via <UserDisplay user={remoofer} />
          </span>
        </div>
      )}
      <div className="d-flex">
        <div className="">
          <UserPicture user={moof.user} />
        </div>
        <div className="col-11">
          <div>
            <p>
              <UserDisplay includeFullName user={moof.user} />
            </p>
            <p>{moof.content}</p>
            <ParentMoof moof={moof} remoofer={moof.user} />
          </div>
          <div className="btn btn-group px-0">
            {actionMoof && hideActions !== true && (
              <React.Fragment>
                <ActionBtn
                  moof={actionMoof}
                  didPerformAction={handlePerformAction}
                  action={{ type: "like", display: "Likes" }}
                />
                <ActionBtn
                  moof={actionMoof}
                  didPerformAction={handlePerformAction}
                  action={{ type: "unlike", display: "Unlike" }}
                />
                <ActionBtn
                  moof={actionMoof}
                  didPerformAction={handlePerformAction}
                  action={{ type: "remoof", display: "Remoof" }}
                />
              </React.Fragment>
            )}
            {isDetail === true ? null : (
              <button
                className="btn btn-outline-primary btn-sm"
                onClick={handleLink}
              >
                View
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
