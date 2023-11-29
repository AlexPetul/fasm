import React, {Suspense, Fragment, lazy} from 'react';
import {Switch, Redirect, Route} from 'react-router-dom';

import Loader from './components/Loader/Loader';
import AdminLayout from './layouts/AdminLayout';

import GuestGuard from './components/Auth/GuestGuard';
import AuthGuard from './components/Auth/AuthGuard';

export const renderRoutes = (routes = []) => (
    <Suspense fallback={<Loader/>}>
        <Switch>
            {routes.map((route, i) => {
                const Guard = route.guard || Fragment;
                const Layout = route.layout || Fragment;
                const Component = route.component;

                return (
                    <Route
                        key={i}
                        path={route.path}
                        exact={route.exact}
                        render={(props) => (
                            <Guard>
                                <Layout>{route.routes ? renderRoutes(route.routes) : <Component {...props} />}</Layout>
                            </Guard>
                        )}
                    />
                );
            })}
        </Switch>
    </Suspense>
);

const routes = [
    {
        exact: true,
        guard: GuestGuard,
        path: '/auth/signin',
        component: lazy(() => import('./views/auth/signin/SignIn2'))
    },
    {
        path: '*',
        layout: AdminLayout,
        guard: null,
        routes: [
            {
                exact: true,
                path: '/imperative',
                component: lazy(() => import('./views/imperative/Imperative'))
            },
        ]
    }
];

export default routes;
