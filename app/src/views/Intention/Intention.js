import React, {useEffect, useState} from "react"
import {Button, Card, Col, Row} from "react-bootstrap";
import Content from "../Content/Content";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";


const Intension = () => {
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
                        <b>To want - khaastan (khaa)</b><br/>
                        <b>With noun: mi + khaa + endings</b><br/>
                        <b>With verbs: mi + khaa + endings be(bo) + verb stem</b>
                    </Card.Title>
                    <Card.Text>
                        <Row>
                            <Col lg={6}>She wants food</Col>
                            <Col lg={6}>Oona ghaza mikhaad</Col>
                        </Row>
                        <Row>
                            <Col lg={6}>We want freedom</Col>
                            <Col lg={6}>Maa aazaadi mikhaaim</Col>
                        </Row>
                        <Row>
                            <Col lg={6}>He wants to go home</Col>
                            <Col lg={6}>Oon mikhaad bege khoone</Col>
                        </Row>
                        <Row>
                            <Col lg={6}>I want to know</Col>
                            <Col lg={6}>Man mikhaam bedoonam</Col>
                        </Row>
                        <Row>
                            <Col lg={6}>They want to close the door</Col>
                            <Col lg={6}>Oona mikhaan daaro bebandan</Col>
                        </Row>
                        <Row>
                            <Col lg={6}>I want to do sport</Col>
                            <Col lg={6}>Man mikhaam varzesh bokonam</Col>
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
                name="Intention (to want)"
                rules={rules}
                setShowInfo={setShowCard}
                sectionId={sectionId}
            /> : null
    )
}

export default Intension