import React, {useEffect, useState} from "react"
import {Button, Card, Col, Row} from "react-bootstrap";
import Content from "../Content/Content";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";


const Modals = () => {
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
                        <b>should / must - baayad</b><br/>
                    </Card.Title>
                    <Card.Text>
                        <Row>
                            <Col lg={6}>I must know</Col>
                            <Col lg={6}>Man baayad bedoonam</Col>
                        </Row>
                        <Row>
                            <Col lg={6}>He should clean his room</Col>
                            <Col lg={6}>Oon baayad otaaghesho tamiz bokone</Col>
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
                name="Modals"
                rules={rules}
                setShowInfo={setShowCard}
                sectionId={sectionId}
            /> : null
    )
}

export default Modals