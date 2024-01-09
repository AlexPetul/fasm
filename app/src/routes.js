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
                path: '/',
                component: lazy(() => import('./views/review-list/ReviewList'))
            },
            {
                exact: true,
                path: '/imperative',
                component: lazy(() => import('./views/imperative/Imperative'))
            },
            {
                exact: true,
                path: '/present-perfect',
                component: lazy(() => import('./views/present-perfect/PresentPerfect'))
            },
            {
                exact: true,
                path: '/present-continues',
                component: lazy(() => import('./views/present-continuos/PresentContinuos'))
            },
            {
                exact: true,
                path: '/intention',
                component: lazy(() => import('./views/Intention/Intention'))
            },
            {
                exact: true,
                path: '/modals',
                component: lazy(() => import('./views/Modals/Modals'))
            },
            {
                exact: true,
                path: '/can-able-to',
                component: lazy(() => import('./views/can-be-able/CanBeAble'))
            },
            {
                exact: true,
                path: '/past-simple',
                component: lazy(() => import('./views/past-simple/PastSimple'))
            },
            {
                exact: true,
                path: '/future-simple',
                component: lazy(() => import('./views/future-simple/FutureSimple'))
            },
            {
                exact: true,
                path: '/past-continues',
                component: lazy(() => import('./views/past-continues/PastContinues'))
            },
            {
                exact: true,
                path: '/dictionary',
                component: lazy(() => import('./views/dictionary/Dictionary'))
            },
        ]
    }
];

export default routes;
