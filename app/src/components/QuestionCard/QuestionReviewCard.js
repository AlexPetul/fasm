import React, {useEffect, useState} from "react"
import {Button, Card, Form, Col, DropdownButton, Dropdown, Row} from "react-bootstrap";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";


const CustomToggle = React.forwardRef(({children, onClick}, ref) => (
    <a
        href=""
        ref={ref}
        onClick={(e) => {
            e.preventDefault();
            onClick(e);
        }}
    >
        {children}
        <i className="feather icon-menu pointer-event"/>
    </a>
));


const QuestionReviewCard = ({data}) => {
    const [showComment, setShowComment] = useState(data.reviewer_answer !== null)
    const [reviewerAnswer, setReviewerAnswer] = useState(data.reviewer_answer)
    const account = useSelector((state) => state.account)

    const save = () => {
        axios.patch(API_SERVER + `sections/${data.section_id}/questions/${data.id}`, {reviewer_answer: reviewerAnswer}, {
            headers: {Authorization: `Bearer ${account.token}`}
        })
            .then(response => {

            })
            .catch(error => {
            })
    }

    return (
        <Row>
            <Col lg={12}>
                <Card className="m-3 pt-3">
                    <Card.Body className="pt-50">
                        <Card.Title className="d-flex justify-content-between">
                            <div className="pr-2">
                                <span>{data.content}</span>
                            </div>
                            <Dropdown alignRight={true}>
                                <Dropdown.Toggle as={CustomToggle}>
                                </Dropdown.Toggle>

                                <Dropdown.Menu>
                                    <Dropdown.Item
                                        href="#"
                                        onClick={() => setShowComment(true)}
                                    >
                                        Add comment
                                    </Dropdown.Item>
                                </Dropdown.Menu>
                            </Dropdown>
                        </Card.Title>
                        <Form>
                            <Form.Group>
                                <Form.Control
                                    as="textarea"
                                    rows={3}
                                    readOnly={true}
                                    value={data.user_answer}
                                />
                            </Form.Group>
                            {showComment ?
                                <Form.Group>
                                    <Form.Control
                                        as="textarea"
                                        rows={3}
                                        onBlur={() => save()}
                                        onChange={(e) => setReviewerAnswer(e.target.value)}
                                        value={reviewerAnswer}
                                    />
                                </Form.Group> : null}
                        </Form>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
    )
}

export default QuestionReviewCard