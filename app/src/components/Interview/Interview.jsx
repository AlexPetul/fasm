import React, {Component} from "react";
import "./Interview.css"

import {withRouter} from "../../common/with-router";


class Interview extends Component {

    render() {
        return (
            <>
                <div className="w3-sidebar w3-bar-block" style="width:25%">
                    <a href="#" className="w3-bar-item w3-button">Link 1</a>
                    <a href="#" className="w3-bar-item w3-button">Link 2</a>
                    <a href="#" className="w3-bar-item w3-button">Link 3</a>
                </div>

                <div style="margin-left:25%">
                    ... page content ...
                </div>
            </>
        );
    }
}

export default withRouter(Interview);