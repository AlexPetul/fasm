import React, {useState} from 'react';
import {ListGroup, Dropdown} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {API_SERVER} from "../../../../config/constant";
import axios from "../../../../utils/axios";
import {LOGOUT} from "../../../../store/actions";
import {useDispatch, useSelector} from "../../../../store";
import Redirect from "react-router-dom/es/Redirect";
import Spinner from "../../../../components/Spinner/Spinner";

const NavRight = () => {
    const account = useSelector((state) => state.account);
    const {isLoggedIn} = account;
    const dispatcher = useDispatch();
    const [loading, setLoading] = useState(false);

    const handleLogout = () => {
        setLoading(true)
        axios
            .post(API_SERVER + 'auth/logout', {}, {headers: {Authorization: `${account.token}`}})
            .then(function (response) {
                dispatcher({type: LOGOUT});
                setLoading(false);
            })
            .catch(function (error) {
                console.log('error - ', error);
                setLoading(false);
            });
    };

    if (!isLoggedIn) {
        return <Redirect to="/auth/signin"/>
    }

    return (
        <div className="navbar pcoded-header navbar-expand-lg navbar-default justify-content-end">
            {loading ? <Spinner/> : null}
            <ListGroup as="ul" bsPrefix=" " className="navbar-nav ml-auto">
                <ListGroup.Item as="li" bsPrefix=" ">
                    <Dropdown className="drp-user">
                        <Dropdown.Toggle as={Link} variant="link" to="#" id="dropdown-basic">
                            <i className="icon feather icon-user"/>
                            <span> {account.user.username} </span>
                        </Dropdown.Toggle>
                        <Dropdown.Menu alignRight className="profile-notification">
                            <ListGroup as="ul" bsPrefix=" " variant="flush" className="pro-body">
                                <ListGroup.Item as="li" bsPrefix=" ">
                                    <Link to="#" className="dropdown-item" onClick={handleLogout}>
                                        <i className="feather icon-log-out"/> Logout
                                    </Link>
                                </ListGroup.Item>
                            </ListGroup>
                        </Dropdown.Menu>
                    </Dropdown>
                </ListGroup.Item>
            </ListGroup>
        </div>
    );
};

export default NavRight;
