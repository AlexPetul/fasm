import React, {useEffect, useState} from "react"
import {Card, Col, Row} from "react-bootstrap";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";
import Spinner from "../../components/Spinner/Spinner";
import QuestionReviewCard from "../../components/QuestionCard/QuestionReviewCard";


const Dictionary = () => {
    const account = useSelector((state) => state.account);
    const [verbs, setVerbs] = useState([])
    const [vocabulary, setVocabulary] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        axios.get(API_SERVER + `dictionary/verbs`, {headers: {Authorization: `Bearer ${account.token}`}})
            .then(response => {
                setVerbs(response.data)
                setIsLoading(false);
            })
            .catch(error => {
                setIsLoading(false);
            })
    }, [])

    useEffect(() => {
        axios.get(API_SERVER + `dictionary/vocabulary`, {headers: {Authorization: `Bearer ${account.token}`}})
            .then(response => {
                setVocabulary(response.data)
                setIsLoading(false);
            })
            .catch(error => {
                setIsLoading(false);
            })
    }, [])

    return (
        <div>
            {isLoading ? <Spinner/> : null}
            <Row>
                <Col lg={12}>
                    <div className="d-inline-block"><h3>Dictionary</h3></div>
                </Col>
            </Row>
            <Row>
                <Card className="col-lg-12">
                    <Card.Header>
                        <Card.Title as="h4">Verbs</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        {verbs.map((x) =>
                            <Row>
                                <Col lg={4}>
                                    <div>{x.eng}</div>
                                </Col>
                                <Col lg={8}>
                                    <div>{x.farsi} ({x.stem})</div>
                                </Col>
                            </Row>
                        )}
                    </Card.Body>
                </Card>
                <Card className="col-lg-12">
                    <Card.Header>
                        <Card.Title as="h4">Prepositions</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        {vocabulary.filter(x => x.preposition === true).map((x) =>
                            <Row>
                                <Col lg={4}>
                                    <div>{x.eng}</div>
                                </Col>
                                <Col lg={8}>
                                    <div>{x.farsi}</div>
                                </Col>
                            </Row>
                        )}
                    </Card.Body>
                </Card>
                <Card className="col-lg-12">
                    <Card.Header>
                        <Card.Title as="h4">Vocabulary</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        {vocabulary.filter((x) => x.preposition === false).map((x) =>
                            <Row>
                                <Col lg={4}>
                                    <div>{x.eng}</div>
                                </Col>
                                <Col lg={8}>
                                    <div>{x.farsi}</div>
                                </Col>
                            </Row>
                        )}
                    </Card.Body>
                </Card>
            </Row>
        </div>
    )
}

export default Dictionary;