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
    const [data, setData] = useState({examples: []})

    useEffect(() => {
        axios.get(API_SERVER + 'sections', {headers: {Authorization: `Bearer ${account.token}`}})
            .then(response => {
                const sectionId = response.data.filter((x) => x.slug === window.location.pathname.slice(1))[0].id
                setSectionId(sectionId)
                axios.get(API_SERVER + `sections/${sectionId}/rules`, {headers: {Authorization: `Bearer ${account.token}`}})
                    .then(response => {
                        setData(response.data)
                    })
            })
    }, [])

    const rules = (
        <div className={`slide-card ${showCard ? 'show' : ''}`} style={{zIndex: 100}}>
            <Card style={{minWidth: "30rem", height: "calc(100vh - 100px)"}}>
                <Card.Body>
                    <Card.Title>
                        <b>{data.grammar}</b><br/>
                    </Card.Title>
                    <Card.Text>
                        {data.examples.map((x) =>
                            <Row>
                                <Col lg={6}>{x.eng}</Col>
                                <Col lg={6}>{x.farsi}</Col>
                            </Row>
                        )}
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