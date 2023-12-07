import React, {useContext, useEffect, useState} from 'react';

import {ConfigContext} from '../../../contexts/ConfigContext';
import useWindowSize from '../../../hooks/useWindowSize';

import axios from "axios";
import {API_SERVER} from "../../../config/constant";
import {useSelector} from "react-redux";
import {ListGroup} from "react-bootstrap";
import {NavLink} from "react-router-dom";

const Navigation = () => {
    const configContext = useContext(ConfigContext);
    const {collapseMenu} = configContext.state;
    const windowSize = useWindowSize();
    const [navigation, setNavigation] = useState([]);
    const account = useSelector((state) => state.account);

    useEffect(() => {
        if (account.user && account.user.role === "student") {
            axios.get(API_SERVER + 'sections', {headers: {Authorization: `Bearer ${account.token}`}})
                .then(response => {
                    setNavigation(response.data);
                })
        }
    }, []);

    let navClass = [
        'pcoded-navbar',
        'menupos-static',
        'menu-dark',
        'navbar-default',
        'brand-default',
        'drp-icon-style1',
        'menu-item-icon-style1',
        'active-default',
        'title-default'
    ];

    if (windowSize.width < 992 && collapseMenu) {
        navClass = [...navClass, 'mob-open'];
    } else if (collapseMenu) {
        navClass = [...navClass, 'navbar-collapsed'];
    }

    let navStyle;

    let navBarClass = ['navbar-wrapper'];

    return (
        <React.Fragment>
            <nav className={navClass.join(' ')} style={navStyle}>
                <div className={navBarClass.join(' ')}>
                    <div className="navbar-content datta-scroll text-center">
                        <ListGroup variant="flush" as="ul" bsPrefix=" " className="nav pcoded-inner-navbar"
                                   id="nav-ps-next">
                            {navigation.map((x) =>
                                <ListGroup.Item as="li" bsPrefix=" " className="">
                                    <NavLink to={x.slug} className="nav-link" exact={true} >
                                        {x.name}
                                    </NavLink>
                                </ListGroup.Item>
                            )}
                        </ListGroup>
                    </div>
                </div>
            </nav>
        </React.Fragment>
    );
};

export default Navigation;
