import React, {useEffect, useState} from "react"
import {Button, Card, Col, DropdownButton, Dropdown, Row, Modal, Form} from "react-bootstrap";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";
import Spinner from "../../components/Spinner/Spinner";
import QuestionCard from "../../components/QuestionCard/QuestionCard";


function QuestionModal(props) {
    return (
        <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Question
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            value={props.question}
                            onChange={props.onCustomQuestion}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.onHide}>Create</Button>
            </Modal.Footer>
        </Modal>
    );
}


const Content = ({name, rules, sectionId, setShowInfo}) => {
    const account = useSelector((state) => state.account);
    const [questions, setQuestions] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [selected, setSelected] = useState([])
    const [modalShow, setModalShow] = useState(false);
    const [customQuestion, setCustomQuestion] = useState("");

    const fetchQuestions = () => {
        axios.get(API_SERVER + `sections/${sectionId}/questions`, {headers: {Authorization: `Bearer ${account.token}`}})
            .then(response => {
                setQuestions(response.data)
                setIsLoading(false);
            })
            .catch(error => {
                setIsLoading(false);
            })
    }

    useEffect(() => {
        fetchQuestions()
    }, [])

    const generate = (type) => {
        setIsLoading(true);
        axios.post(API_SERVER + `sections/${sectionId}/questions`, {type: type},
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

    const generateManually = () => {
        setModalShow(false);
        setIsLoading(true);
        axios.post(API_SERVER + `sections/${sectionId}/questions`, {content: customQuestion},
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

    const onSelect = (id) => {
        setSelected([id, ...selected]);
    }

    const onDeSelect = (id) => {
        setSelected(selected.filter((x) => x !== id))
    }

    const markForReview = () => {
        setIsLoading(true);
        axios.patch(API_SERVER + `sections/${sectionId}/questions/${selected[0]}`,
            {
                for_review: true
            },
            {
                headers: {Authorization: `Bearer ${account.token}`}
            },

        )
            .then(response => {
                fetchQuestions()
                setIsLoading(false);
            })
            .catch(error => {
                setIsLoading(false);
            })
    }

    return (
        <div>
            {isLoading ? <Spinner/> : null}
            <Row>
                <Col lg={11}>
                    <div className="d-inline-block"><h3>{name}</h3></div>
                    <div className="d-inline-block ml-5">
                        <DropdownButton id="dropdown-basic-button" title="Generate">
                            <Dropdown.Item href="#" onClick={() => generate("sentence")}>Sentence</Dropdown.Item>
                            <Dropdown.Item href="#" onClick={() => generate("story")}>Story</Dropdown.Item>
                            <Dropdown.Item href="#" onClick={() => setModalShow(true)}>Manually</Dropdown.Item>
                        </DropdownButton>
                    </div>
                    <div className="d-inline-block ml-5">
                        <Button
                            className="btn-block"
                            color="danger"
                            variant={selected.length === 0 ? 'dark' : 'primary'}
                            size="large"
                            disabled={selected.length === 0}
                            onClick={markForReview}
                        >
                            Review {selected.length ? selected.length : null}
                        </Button>
                    </div>
                </Col>
                <Col lg={1} className="order-last">
                    <Button
                        className="btn-block"
                        color="primary"
                        size="large"
                        type="submit"
                        variant="primary"
                        onClick={() => setShowInfo(true)}
                    >
                        Info
                    </Button>
                    {rules}
                </Col>
            </Row>
            {questions.map((data) =>
                <QuestionCard
                    data={data}
                    sectionId={sectionId}
                    onDelete={onDelete}
                    onSelect={onSelect}
                    onDeSelect={onDeSelect}
                />
            )}
            <QuestionModal
                show={modalShow}
                question={customQuestion}
                onCustomQuestion={(e) => setCustomQuestion(e.target.value)}
                onHide={() => generateManually()}
            />
        </div>
    )
}

export default Content;