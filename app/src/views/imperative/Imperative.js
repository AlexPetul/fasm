import React, {useEffect, useState} from "react"
import {Button, Card, Col, DropdownButton, Dropdown, Row} from "react-bootstrap";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";
import Spinner from "../../components/Spinner/Spinner";
import QuestionCard from "../../components/QuestionCard/QuestionCard";


const Imperative = () => {
    const [showCard, setShowCard] = useState(false);
    const account = useSelector((state) => state.account);
    const [questions, setQuestions] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        axios.get(API_SERVER + `sections/${1}/questions`, {headers: {Authorization: `Bearer ${account.token}`}})
            .then(response => {
                setQuestions(response.data)
                setIsLoading(false);
            })
            .catch(error => {
                setIsLoading(false);
            })
    }, [])

    const generate = (type) => {
        setIsLoading(true);
        axios.post(API_SERVER + `sections/${1}/questions`, {type: type},
            {
                headers: {Authorization: `Bearer ${account.token}`}
            }
        )
            .then(response => {
                setQuestions([response.data, ...questions]);
                setIsLoading(false);
            })
            .catch(error => {
                setIsLoading(false);
            })
    }

    const onDelete = (id) => {
        setQuestions(questions.filter((x) => x.id !== id));
    }


    return (
        <div>
            {isLoading ? <Spinner/> : null}
            <Row>
                <Col lg={11}>
                    <div className="d-inline-block"><h3>Imperative</h3></div>
                    <div className="d-inline-block ml-5">
                        <DropdownButton id="dropdown-basic-button" title="Generate">
                            <Dropdown.Item href="#" onClick={() => generate("sentence")}>Sentence</Dropdown.Item>
                            <Dropdown.Item href="#" onClick={() => generate("story")}>Story</Dropdown.Item>
                        </DropdownButton>
                    </div>
                </Col>
                <Col lg={1} className="order-last">
                    <Button
                        className="btn-block"
                        color="primary"
                        size="large"
                        type="submit"
                        variant="primary"
                        onClick={() => setShowCard(!showCard)}
                    >
                        Info
                    </Button>
                    <div className={`slide-card ${showCard ? 'show' : ''}`}>
                        <Card style={{minWidth: "30rem", height: "calc(100vh - 100px)"}}>
                            <Card.Body>
                                <Card.Title>
                                    <b>be (bo) + verb stem</b><br/>
                                    <b>na + verb stem</b>
                                </Card.Title>
                                <Card.Text>
                                    <Row>
                                        <Col lg={6}>Dont study much</Col>
                                        <Col lg={6}>Kheili dars nakon</Col>
                                    </Row>
                                    <Row>
                                        <Col lg={6}>Be happy</Col>
                                        <Col lg={6}>Khoshhal baash</Col>
                                    </Row>
                                    <Row>
                                        <Col lg={6}>Look at him</Col>
                                        <Col lg={6}>Oono <b>be</b>bin</Col>
                                    </Row>
                                    <Row>
                                        <Col lg={6}>Drink a lot of water</Col>
                                        <Col lg={6}>Aab ziyaad <b>bo</b>khor</Col>
                                    </Row>
                                    <Row>
                                        <Col lg={6}>Watch films</Col>
                                        <Col lg={6}>Film <b>be</b>bin</Col>
                                    </Row>
                                </Card.Text>
                                <Button style={{bottom: 20, width: "calc(100% - 45px)"}} className="position-absolute"
                                        variant="primary" onClick={() => setShowCard(false)}>Close</Button>
                            </Card.Body>
                        </Card>
                    </div>
                </Col>
            </Row>
            {questions.map((data) =>
                <QuestionCard
                    data={data}
                    onDelete={onDelete}
                />
            )}
        </div>
    )
}

export default Imperative