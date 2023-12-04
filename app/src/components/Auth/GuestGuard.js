import React from 'react';
import { Redirect } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { BASE_URL } from '../../config/constant';

const GuestGuard = ({ children }) => {
    const account = useSelector((state) => state.account);
    const { isLoggedIn } = account;

    if (isLoggedIn) {
        if (account.user.role === "student") {
            return <Redirect to={BASE_URL}/>;
        } else {
            return <Redirect to="/"/>;
        }
    }

    return <React.Fragment>{children}</React.Fragment>;
};

export default GuestGuard;
