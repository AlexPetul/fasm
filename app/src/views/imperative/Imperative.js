import React, {useEffect, useState} from "react"
import {Button, Card, Col, Row} from "react-bootstrap";
import Content from "../Content/Content";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";


const Imperative = () => {
    const account = useSelector((state) => state.account);
    const [showCard, setShowCard] = useState(false);
    const [sectionId, setSectionId] = useState()

    useEffect(() => {
        axios.get(API_SERVER + 'sections', {headers: {Authorization: `Bearer ${account.token}`}})
            .then(response => {
                setSectionId(response.data.filter((x) => x.slug === window.location.pathname.slice(1))[0].id)
            })
    }, [])

    const rules = (
        <div className={`slide-card ${showCard ? 'show' : ''}`} style={{zIndex: 100}}>
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
    )

    return (
        sectionId ?
            <Content
                name="Imperative"
                rules={rules}
                setShowInfo={setShowCard}
                sectionId={sectionId}
            /> : null
    )
}

export default Imperative