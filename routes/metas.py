from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.metas import Metas

metas_bp = Blueprint('metas', __name__)


