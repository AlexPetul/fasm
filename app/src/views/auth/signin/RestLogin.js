import React, {useState} from 'react';
import {useDispatch} from 'react-redux';
import {Row, Col, Button, Alert} from 'react-bootstrap';

import * as Yup from 'yup';
import {Formik} from 'formik';
import axios from 'axios';
import useScriptRef from '../../../hooks/useScriptRef';
import {API_SERVER} from './../../../config/constant';
import {ACCOUNT_INITIALIZE} from './../../../store/actions';
import Spinner from "../../../components/Spinner/Spinner";

const RestLogin = ({className, ...rest}) => {
    const dispatcher = useDispatch();
    const scriptedRef = useScriptRef();
    const [loading, setLoading] = useState(false)

    return (
        <React.Fragment>
            {loading ? <Spinner/> : null}
            <Formik
                initialValues={{
                    username: '',
                    password: '',
                    submit: null
                }}
                validationSchema={Yup.object().shape({
                    password: Yup.string().max(255).required('Password is required')
                })}
                onSubmit={async (values, {setErrors, setStatus, setSubmitting}) => {
                    setLoading(true);
                    try {
                        axios
                            .post(API_SERVER + 'auth/login/', {
                                password: values.password,
                                username: values.username
                            })
                            .then(function (response) {
                                if (response.data.access) {
                                    const access = response.data.access;
                                    axios.get(API_SERVER + 'auth/me', {
                                        headers: {Authorization: `Bearer ${access}`}
                                    }).then(response => {
                                        dispatcher({
                                            type: ACCOUNT_INITIALIZE,
                                            payload: {
                                                isLoggedIn: true,
                                                user: response.data,
                                                token: access,
                                            }
                                        });
                                        if (scriptedRef.current) {
                                            setStatus({success: true});
                                            setSubmitting(false);
                                            setLoading(false);
                                        }
                                    });
                                } else {
                                    setStatus({success: false});
                                    setErrors({submit: response.data.detail});
                                    setSubmitting(false);
                                    setLoading(false);
                                }
                            })
                            .catch(function (error) {
                                console.log(error);
                                setStatus({success: false});
                                setErrors({submit: error.response.data.detail});
                                setSubmitting(false);
                                setLoading(false);
                            });
                    } catch (err) {
                        console.error(err);
                        if (scriptedRef.current) {
                            setStatus({success: false});
                            setErrors({submit: err.message});
                            setSubmitting(false);
                            setLoading(false);
                        }
                    }
                }}
            >
                {({errors, handleBlur, handleChange, handleSubmit, isSubmitting, touched, values}) => (
                    <form noValidate onSubmit={handleSubmit} className={className} {...rest}>
                        <div className="form-group mb-3">
                            <input
                                className="form-control"
                                error={touched.username && errors.username}
                                label="Username"
                                placeholder="Username"
                                name="username"
                                onBlur={handleBlur}
                                onChange={handleChange}
                                value={values.username}
                            />
                            {touched.username && errors.username &&
                                <small className="text-danger form-text">{errors.username}</small>}
                        </div>
                        <div className="form-group mb-4">
                            <input
                                className="form-control"
                                error={touched.password && errors.password}
                                label="Password"
                                placeholder="Password"
                                name="password"
                                onBlur={handleBlur}
                                onChange={handleChange}
                                type="password"
                                value={values.password}
                            />
                            {touched.password && errors.password &&
                                <small className="text-danger form-text">{errors.password}</small>}
                        </div>

                        {errors.submit && (
                            <Col sm={12}>
                                <Alert variant="danger">{errors.submit}</Alert>
                            </Col>
                        )}

                        <Row>
                            <Col mt={2}>
                                <Button
                                    className="btn-block"
                                    color="primary"
                                    disabled={isSubmitting}
                                    size="large"
                                    type="submit"
                                    variant="primary"
                                >
                                    Sign IN
                                </Button>
                            </Col>
                        </Row>
                    </form>
                )}
            </Formik>
        </React.Fragment>
    );
};

export default RestLogin;
