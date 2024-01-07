import React, { useContext } from 'react';

import NavRight from './NavRight';

import { ConfigContext } from '../../../contexts/ConfigContext';
import * as actionType from '../../../store/actions';

const NavBar = () => {
    const configContext = useContext(ConfigContext);
    const { collapseMenu } = configContext.state;
    const { dispatch } = configContext;

    let headerClass = ['navbar', 'pcoded-header', 'navbar-expand-lg', 'navbar-default'];

    let toggleClass = ['mobile-menu'];
    if (collapseMenu) {
        toggleClass = [...toggleClass, 'on'];
    }

    const navToggleHandler = () => {
        dispatch({ type: actionType.COLLAPSE_MENU });
    };

    let collapseClass = ['collapse navbar-collapse'];

    let navBar = (
        <React.Fragment>
            <div className={collapseClass.join(' ')}>
                <NavRight />
            </div>
        </React.Fragment>
    );

    return (
        <React.Fragment>
            <header className={headerClass.join(' ')}>{navBar}</header>
        </React.Fragment>
    );
};

export default NavBar;
