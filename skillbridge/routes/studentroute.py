from flask import request, jsonify, Blueprint
from services import student_service as s
from utilities import to_json
from flasgger import swag_from
student_endpoint = Blueprint('student_endpoint', __name__)


@student_endpoint.route('/', methods=['GET'])
@swag_from({
    'description': 'Get all students',
    'responses': {
        '200': {
            'description': 'All students retrieved successfully',
        },
    },
})
def get_all_students():
    students = s.get_all_students()
    return to_json(students)


@student_endpoint.route('/<int:student_id>', methods=['GET'])
@swag_from({
    'description': 'Get a student by ID',
    'parameters': [
        {
            'name': 'student_id',
            'in': 'path',
            'type': 'integer',
            'required': 'true',
            'description': 'ID of the student to retrieve',
        }
    ],
    'responses': {
        '200': {
            'description': 'student retrieved successfully',
        },
        '404': {
            'description': 'student not found',
        },
    },
})
def get_student_by_id(student_id):
    student = s.get_student_by_id(student_id)
    if student is None:
        return jsonify({"error": "student not found"}), 404
    return to_json(student)


@student_endpoint.route('/', methods=['POST'])
@swag_from({
    'description': 'Add a new student',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': 'true',
            'schema': {
                'id': 'Student',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Name of the student',
                    },
                },
                'required': ['name']
            },
        }
    ],
    'responses': {
        '201': {
            'description': 'Student created successfully',
        },
        '400': {
            'description': 'Student name is required',
        },
        '400': {
            'description': 'Student already exists',
        },
    },
})
def add_new_student():
    request_data = request.get_json()
    if 'name' not in request_data:
        return jsonify({"error": "Faculty name is required"}), 400
    if s.student_exists(request_data['name']):
        return jsonify({"error": "Student already exists"}), 400
    new_student_id = s.add_new_student(request_data['name'])
    student = s.add_new_student(new_student_id)
    return to_json(student), 201


@student_endpoint.route('/<int:student_id>', methods=['PUT'])
@swag_from({
    'description': 'Update a student',
    'parameters': [
        {
            'name': 'student_id',
            'in': 'path',
            'type': 'integer',
            'required': 'true',
            'description': 'ID of the student to update',
        },
        {
            'name': 'body',
            'in': 'body',
            'required': 'true',
            'schema': {
                'id': 'Student',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'The new name of the Student',
                    },
                },
                'required': ['name']
            },
        }
    ],
    'responses': {
        '200': {
            'description': 'Student updated successfully',
        },
        '400': {
            'description': 'Student name is required',
        },
        '404': {
            'description': 'Student not found',
        },
    },
})
def update_student(student_id):
    request_data = request.get_json()
    if 'name' not in request_data:
        return jsonify({"error": "Student name is required"}), 400
    student = s.get_student_by_id(student_id)
    if (student is None):
        return jsonify({"error": "Student not found"}), 404
    student.name = request_data['name']
    s.update_student(student)
    return to_json(student), 200


@student_endpoint.route('/<int:faculty_id>', methods=['DELETE'])
@swag_from({
    'description': 'Delete a student',
    'parameters': [
        {
            'name': 'stuident_id',
            'in': 'path',
            'type': 'integer',
            'required': 'true',
            'description': 'ID of the student to delete',
        }
    ],
    'responses': {
        '200': {
            'description': 'Student deleted successfully',
        },
        '404': {
            'description': 'Student not found',
        },
    },
})
def delete_student(student_id):
    student = s.get_student_by_id(student_id)
    if (student is None):
        return jsonify({"error": "Student not found"}), 404
    s.delete_student(student_id)
    return jsonify({"message": "Student deleted successfully"}), 200
