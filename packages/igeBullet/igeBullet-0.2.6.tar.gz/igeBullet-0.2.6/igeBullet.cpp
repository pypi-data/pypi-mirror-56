#include <Python.h>
#include <stdio.h>
#include "igeBullet_doc_en.h"
#include "igeBullet.h"
#include <vector>

#include "btBulletDynamicsCommon.h"
#include "BulletCollision/CollisionDispatch/btGhostObject.h"
#include "BulletDynamics/Character/btKinematicCharacterController.h"

#if defined _WIN32             //WIN32
#   include <time.h>
#   include <Windows.h>
#elif defined __APPLE__
#   include "TargetConditionals.h"
#   if TARGET_OS_IPHONE        //iOS
#       include <sys/types.h>
#   else                       //OSX
#       include <time.h>
#   endif
#	include <mach/mach_time.h>
#elif defined __ANDROID__      //Android
#   include <sys/time.h>
#   include <time.h>
#endif

static PyTypeObject* Vec2Type = nullptr;
static PyTypeObject* Vec3Type = nullptr;
static PyTypeObject* Vec4Type = nullptr;
static PyTypeObject* QuatType = nullptr;
static PyTypeObject* Mat22Type = nullptr;
static PyTypeObject* Mat33Type = nullptr;
static PyTypeObject* Mat44Type = nullptr;
typedef struct {
	PyObject_HEAD
		float v[4];
	int d;
} vec_obj;

typedef struct {
	PyObject_HEAD
		float m[16];
	int d;
} mat_obj;

typedef struct {
	PyObject_HEAD
		float min[4];
	float max[4];
	int d;
} aabb_obj;


PyObject* createCollisionShapeGraphicsObject(btCollisionShape* collisionShape);

bool pyObjToVector(PyObject* obj, btVector3& v) {

	if (obj) {
		int d;
		v.m_floats[0] = v.m_floats[1] = v.m_floats[2] = v.m_floats[3] = 0.0f;
		if (obj->ob_type == Vec3Type || obj->ob_type == Vec4Type || obj->ob_type == QuatType) {
			d = ((vec_obj*)(obj))->d;
			for (int j = 0; j < d; j++) {
				v.m_floats[j] = ((vec_obj*)(obj))->v[j];
			}
			return true;
		}
		else if (PyTuple_Check(obj)) {
			d = (int)PyTuple_Size(obj);
			if (d > 4) d = 4;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyTuple_GET_ITEM(obj, j);
				v.m_floats[j] = (float)PyFloat_AsDouble(val);
			}
			return true;
		}
		else if (PyList_Check(obj)) {
			d = (int)PyList_Size(obj);
			if (d > 4) d = 4;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyList_GET_ITEM(obj, j);
				v.m_floats[j] = (float)PyFloat_AsDouble(val);
			}
			return true;
		}
	}
	PyErr_SetString(PyExc_ValueError, "invalid arguments");
	return  false;
}
bool pyObjToTransform(PyObject* obj, btTransform& t) {

	btQuaternion q;

	if (obj) {
		if (PyTuple_Check(obj)) {
			if (PyTuple_Size(obj) != 2) goto error;
			if (!pyObjToVector(PyTuple_GET_ITEM(obj, 0), t.getOrigin())) goto error;
			if (!pyObjToVector(PyTuple_GET_ITEM(obj, 1), *((btVector3*)&q))) goto error;
			t.setRotation(q);
			return true;
		}
		else if (PyList_Check(obj)) {
			if (PyList_Size(obj) != 2) goto error;
			if (!pyObjToVector(PyList_GET_ITEM(obj, 0), t.getOrigin())) goto error;
			if (!pyObjToVector(PyList_GET_ITEM(obj, 1), *((btVector3*)& q))) goto error;
			t.setRotation(q);
			return true;
		}
	}
error:
	PyErr_SetString(PyExc_ValueError, "invalid arguments");
	return  false;
}


//////////////////////////////////////////////////////////////////////
//Constraint
//////////////////////////////////////////////////////////////////////
#if true

/*
POINT2POINT_CONSTRAINT_TYPE = 3,
HINGE_CONSTRAINT_TYPE,
CONETWIST_CONSTRAINT_TYPE,
D6_CONSTRAINT_TYPE,
SLIDER_CONSTRAINT_TYPE,
CONTACT_CONSTRAINT_TYPE,
D6_SPRING_CONSTRAINT_TYPE,
GEAR_CONSTRAINT_TYPE,
FIXED_CONSTRAINT_TYPE,
D6_SPRING_2_CONSTRAINT_TYPE,
*/

PyObject* constraint_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "type", "bodyA","bodyB","pivotA","pivotB","axisA","axisB","frameA","frameB", "anchor", "useReferenceFrameA","ratio","rotOrder",NULL };

	int constrainttype = -1;
	rigidbody_obj* o_bodyA = nullptr;
	rigidbody_obj* o_bodyB = nullptr;
	PyObject* o_pivotA = nullptr;
	PyObject* o_pivotB = nullptr;
	PyObject* o_axisA = nullptr;
	PyObject* o_axisB = nullptr;
	PyObject* o_frameA = nullptr;
	PyObject* o_frameB = nullptr;
	PyObject* o_anchor = nullptr;
	int useReferenceFrameA = false;
	float ratio = 1.0f;
	int rotOrder = RO_XYZ;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "i|OOOOOOOOOpfi", kwlist,
		&constrainttype, 
		&o_bodyA, &o_bodyB, &o_pivotA, &o_pivotB, &o_axisA, &o_axisB, &o_frameA, &o_frameB, &o_anchor, 
		&useReferenceFrameA,&ratio,&rotOrder))
		return NULL;

	btRigidBody* bodyA;
	btRigidBody* bodyB;
	btVector3 pivotA, pivotB, axisA, axisB, anchor;
	btTransform frameA, frameB;

	if (o_bodyA) bodyA = (btRigidBody*)o_bodyA->btbody;
	if (o_bodyB) bodyB = (btRigidBody*)o_bodyB->btbody;
	if (o_pivotA)
		if (!pyObjToVector(o_pivotA, pivotA)) return NULL;
	if (o_pivotB)
		if (!pyObjToVector(o_pivotB, pivotB)) return NULL;
	if (o_axisA)
		if (!pyObjToVector(o_axisA, axisA)) return NULL;
	if (o_axisB)
		if (!pyObjToVector(o_axisB, axisB)) return NULL;
	if (o_frameA)
		if (!pyObjToTransform(o_frameA, frameA)) return NULL;
	if (o_frameB)
		if (!pyObjToTransform(o_frameB, frameB)) return NULL;
	if (o_anchor)
		if (!pyObjToVector(o_anchor, anchor)) return NULL;

	btTypedConstraint* constraint = nullptr;
	switch (constrainttype) {
	case HINGE_CONSTRAINT_TYPE: 				//btHingeConstraint
		if (o_bodyA) {
			if (o_bodyB) {
				if (o_frameA && o_frameB)
					constraint = new btHingeConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
				else if (o_pivotA && o_pivotB && o_axisA && o_axisB)
					constraint = new btHingeConstraint(*bodyA, *bodyB, pivotA, pivotB, axisA, axisB, useReferenceFrameA);
			}
			else {
				if (o_frameA)
					constraint = new btHingeConstraint(*bodyA, frameA, useReferenceFrameA);
				else if (o_pivotA && o_axisA)
					constraint = new btHingeConstraint(*bodyA, pivotA, axisA, useReferenceFrameA);
			}
		}
		break;
	//case HINGE2_CONSTRAINTTYPE:				//btHinge2Constraint
	//	if (o_bodyA && o_bodyB && o_anchor && o_axisA && o_axisB) {
	//		constraint = new btHinge2Constraint(*bodyA, *bodyB, anchor, axisA, axisB);
	//	}
	//	break;
	case GEAR_CONSTRAINT_TYPE:				//btGearConstraint
		if (o_bodyA && o_bodyB && o_axisA && o_axisB) {
			constraint = new btGearConstraint(*bodyA, *bodyB, axisA, axisB, ratio);
		}
		break;
	case POINT2POINT_CONSTRAINT_TYPE:		//btPoint2PointConstraint
		if (o_bodyA && o_pivotA) {
			if (o_bodyB && o_pivotB) {
				constraint = new btPoint2PointConstraint(*bodyA, *bodyB, pivotA, pivotB);
			}
			else {
				constraint = new btPoint2PointConstraint(*bodyA, pivotA);
			}
		}
		break;
	case SLIDER_CONSTRAINT_TYPE:				//btSliderConstraint
		if (o_bodyB && o_frameB) {
			if (o_bodyA && o_frameA) {
				constraint = new btSliderConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
			}
			else {
				constraint = new btSliderConstraint(*bodyB, frameB, useReferenceFrameA);
			}
		}
		break;
	case D6_CONSTRAINT_TYPE:		//btGeneric6DofConstraint
		if (o_bodyB && o_frameB) {
			if (o_bodyA && o_frameA) {
				constraint = new btGeneric6DofConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
			}
			else {
				constraint = new btGeneric6DofConstraint(*bodyB, frameB, useReferenceFrameA);
			}
			break;
	case CONETWIST_CONSTRAINT_TYPE:			//btConeTwistConstraint
		if (o_bodyA && o_frameA) {
			if (o_bodyB && o_frameB) {
				constraint = new btConeTwistConstraint(*bodyA, *bodyB, frameA, frameB);
			}
			else {
				constraint = new btConeTwistConstraint(*bodyA, frameA);
			}
		}
		break;
	//case UNIVERSAL_CONSTRAINTTYPE:			//btUniversalConstraint
	//	if (o_bodyA && o_bodyB && o_anchor && o_axisA && o_axisB) {
	//		constraint = new btUniversalConstraint(*bodyA, *bodyB, anchor, axisA, axisB);
	//	}
	//	break;
	case FIXED_CONSTRAINT_TYPE:				//btFixedConstraint
		if (o_bodyA && o_bodyB && o_frameA && o_frameB) {
			constraint = new btFixedConstraint(*bodyA, *bodyB, frameA, frameB);
		}
		break;
	case D6_SPRING_CONSTRAINT_TYPE:
		if (o_bodyA && o_frameA) {
			if (o_bodyB && o_frameB) {
				constraint = new btGeneric6DofSpringConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
			}
			else {
				constraint = new btGeneric6DofSpringConstraint(*bodyB, frameB, useReferenceFrameA);
			}
		}
		break;
	case D6_SPRING_2_CONSTRAINT_TYPE:	//btGeneric6DofSpring2Constraint
		if (o_bodyA && o_frameA) {
			if (o_bodyB && o_frameB) {
				constraint = new btGeneric6DofSpring2Constraint(*bodyA, *bodyB, frameA, frameB, (RotateOrder)rotOrder);
			}
			else {
				constraint = new btGeneric6DofSpring2Constraint(*bodyB, frameB, (RotateOrder)rotOrder);
			}
		}
		break;
		}
	}

	if (!constraint) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}

	constraint_obj* self = (constraint_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;
	constraint->setUserConstraintPtr(self);
	self->btconstraint = constraint;

	return (PyObject*)self;
}

void  constraint_dealloc(constraint_obj* self)
{
	//if (self->btshape) delete ((btCollisionShape*)(self->btshape));
	Py_TYPE(self)->tp_free(self);
}

PyObject* constraint_str(constraint_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics constrain object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* constraint_setLimit(constraint_obj* self, PyObject* args) {

	btScalar low;
	btScalar high;
	int axis = 0;
	btScalar _softness = 1.f;
	btScalar _biasFactor = 0.3f;
	btScalar _relaxationFactor = 1.0f;


	switch (((btTypedConstraint*)(self->btconstraint))->getConstraintType()) {
	case HINGE_CONSTRAINT_TYPE: 		//btHingeConstraint
		_softness = 0.9f;
		if (!PyArg_ParseTuple(args, "ff|fff", &low, &high, &_softness, &_biasFactor, &_relaxationFactor)) return NULL;
		((btHingeConstraint*)(self->btconstraint))->setLimit(low, high, _softness, _biasFactor, _relaxationFactor);
		break;
	case GEAR_CONSTRAINT_TYPE:			//btGearConstraint
		break;
	case POINT2POINT_CONSTRAINT_TYPE:	//btPoint2PointConstraint
		break;
	case SLIDER_CONSTRAINT_TYPE:		//btSliderConstraint
		break;
	case D6_CONSTRAINT_TYPE:			//btGeneric6DofConstraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btGeneric6DofConstraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	case CONETWIST_CONSTRAINT_TYPE:		//btConeTwistConstraint
	{
		PyObject* arg1;
		btScalar val2;
		btScalar val3 = FLT_MAX;
		if (!PyArg_ParseTuple(args, "Of|ffff", &arg1, &val2, &val3, &_softness, &_biasFactor, &_relaxationFactor)) return NULL;
		if (val3 == FLT_MAX) {
			int limitIndex = (int)PyLong_AsLong(arg1);
			((btConeTwistConstraint*)(self->btconstraint))->setLimit(limitIndex, val2);
		}
		else {
			btScalar val1 = (btScalar)PyFloat_AsDouble(arg1);
			((btConeTwistConstraint*)(self->btconstraint))->setLimit(val1, val2, val3, _softness, _biasFactor, _relaxationFactor);
		}
	}
		break;
	case FIXED_CONSTRAINT_TYPE:			//btFixedConstraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btFixedConstraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	case D6_SPRING_CONSTRAINT_TYPE:		//btGeneric6DofSpringConstraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btGeneric6DofSpringConstraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	case D6_SPRING_2_CONSTRAINT_TYPE:	//btGeneric6DofSpring2Constraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btGeneric6DofSpring2Constraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	}


}


PyMethodDef constraint_methods[] = {
	{ "setLimit", (PyCFunction)constraint_setLimit, METH_VARARGS, setLimit_doc},
	{ NULL,	NULL }
};

PyGetSetDef constraint_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject ConstraintType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.constraint",				/* tp_name */
	sizeof(constraint_obj),             /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)constraint_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)constraint_str,           /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	constraint_doc,						/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	constraint_methods,					/* tp_methods */
	0,                                  /* tp_members */
	constraint_getsets,                 /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	constraint_new,						/* tp_new */
	0,									/* tp_free */
};



#endif


//////////////////////////////////////////////////////////////////////
//Shape
//////////////////////////////////////////////////////////////////////
#if true

PyObject* shape_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "type","radius","height","halfExtents","normal","constant", NULL };
	int shapetype;
	float radius=1.0f;
	float height = 1.0f;
	PyObject* halfExtents = nullptr;
	PyObject* normal = nullptr;
	float constant = 0.0f;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "i|ffOOf", kwlist,
		&shapetype, &radius, &height, &halfExtents, &normal, &constant))
		return NULL;

	btVector3 v;
	btScalar f;
	btCollisionShape* shape=nullptr;

	switch (shapetype) {
	case BOX_SHAPE_PROXYTYPE:
		if (!pyObjToVector(halfExtents, v)) return NULL;
		shape = new btBoxShape(v);
		break;
	case SPHERE_SHAPE_PROXYTYPE:
		shape = new btSphereShape(radius);
		break;
	case CAPSULE_SHAPE_PROXYTYPE:
		shape = new btCapsuleShape(radius, height);
		break;
	case CONE_SHAPE_PROXYTYPE:
		shape = new btConeShape(radius, height);
		break;
	case CYLINDER_SHAPE_PROXYTYPE:
		if (!pyObjToVector(halfExtents, v)) return NULL;
		shape = new btCylinderShape(v);
		break;
	case STATIC_PLANE_PROXYTYPE:
		if (!pyObjToVector(normal, v)) return NULL;
		shape = new btStaticPlaneShape(v, constant);
		break;
	case COMPOUND_SHAPE_PROXYTYPE:
		shape = new btCompoundShape();
		break;
	}
	shape_obj* self = (shape_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;
	self->btshape = shape;

	shape->setUserPointer(self);

	return (PyObject*)self;
}

void  shape_dealloc(shape_obj* self)
{
	if(self->btshape) delete ((btCollisionShape*)(self->btshape));
	Py_TYPE(self)->tp_free(self);
}

PyObject* shape_str(shape_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics shape object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* shape_getMeshData(shape_obj* self, PyObject* args) {
	return createCollisionShapeGraphicsObject((btCollisionShape*)self->btshape);
}


PyMethodDef shape_methods[] = {
	{ "getMeshData", (PyCFunction)shape_getMeshData, METH_VARARGS, getMeshData_doc},
	{ NULL,	NULL }
};

PyGetSetDef shape_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject ShapeType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.shape",					/* tp_name */
	sizeof(shape_obj),                  /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)shape_dealloc,			/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)shape_str,                /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	shape_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	shape_methods,						/* tp_methods */
	0,                                  /* tp_members */
	shape_getsets,                      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	shape_new,							/* tp_new */
	0,									/* tp_free */
};
#endif
//////////////////////////////////////////////////////////////////////
//Rigidbody
//////////////////////////////////////////////////////////////////////
#if true
PyObject* rigidbody_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "shape","mass","pos","rot","activate", NULL };

	shape_obj* shape_o = nullptr;
	PyObject* mass_o = nullptr;
	PyObject* pos_o = nullptr;
	PyObject* rot_o = nullptr;
	int activate = 1;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "OO|OOi", kwlist,
		&shape_o, &mass_o, &pos_o, &rot_o, &activate))
		return NULL;


	btCollisionShape* shape = nullptr;

	btTransform transform;
	transform.setIdentity();

	if (pos_o) {
		if (!pyObjToVector(pos_o, transform.getOrigin())) return NULL;
	}
	if (rot_o) {
		btQuaternion q;
		if (!pyObjToVector(rot_o, *((btVector3*)(&q)))) return NULL;
		transform.setRotation(q);
	}
	float mass = (float)PyFloat_AsDouble(mass_o);
	bool isDynamic = (mass != 0.f);

	btVector3 localInertia(0, 0, 0);
	if (isDynamic) ((btCollisionShape*)(shape_o->btshape))->calculateLocalInertia(mass, localInertia);

	btDefaultMotionState* motionState = new btDefaultMotionState(transform);
	btRigidBody::btRigidBodyConstructionInfo rbInfo(mass, motionState, ((btCollisionShape*)(shape_o->btshape)), localInertia);
	rbInfo.m_restitution = 0.0f;
	rbInfo.m_friction = 0.5f;
	rbInfo.m_linearDamping = 0.03f;
	rbInfo.m_angularDamping = 0.03f;

	btRigidBody* body = new btRigidBody(rbInfo);
	if(!activate)
		body->forceActivationState(WANTS_DEACTIVATION);

	body->setContactProcessingThreshold(BT_LARGE_FLOAT);
	if (!isDynamic) body->setCollisionFlags(body->getCollisionFlags() | btCollisionObject::CF_STATIC_OBJECT);

	rigidbody_obj* self = (rigidbody_obj*)type->tp_alloc(type, 0);

	self->btbody = body;
	
	if (isDynamic) {
		self->collisionGroup = 1;
		self->collisionMask = -1;
	}
	else {
		self->collisionGroup = 2;
		self->collisionMask = 3;
	}
	if (body->getBroadphaseHandle()) {
		body->getBroadphaseHandle()->m_collisionFilterGroup = self->collisionGroup;
		body->getBroadphaseHandle()->m_collisionFilterMask = self->collisionMask;
	}

	Py_INCREF(shape_o);
	
	body->setUserPointer(self);



	return (PyObject*)self;
}

void  rigidbody_dealloc(rigidbody_obj* self)
{
	if (self->btbody) {
		btCollisionShape* shape = ((btRigidBody*)(self->btbody))->getCollisionShape();
		shape_obj* shapeobj = (shape_obj*)shape->getUserPointer();
		Py_DECREF(shapeobj);
		delete ((btRigidBody*)(self->btbody));
	}
	Py_TYPE(self)->tp_free(self);
}

PyObject* rigidbody_str(rigidbody_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics rigidbody object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

PyObject* rigidbody_getposition(rigidbody_obj* self)
{
	btVector3& pos = ((btRigidBody*)self->btbody)->getWorldTransform().getOrigin();
	PyObject* out = PyTuple_New(3);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(pos.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(pos.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(pos.getZ()));
	return out;
}
int rigidbody_setposition(rigidbody_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector(value, v)) return NULL;
	btTransform& trans = ((btRigidBody*)self->btbody)->getWorldTransform();
	trans.setOrigin(v);
	//if (world) world->GetWorld()->updateSingleAabb(object);
	return 0;
}

PyObject* rigidbody_getrotation(rigidbody_obj* self)
{
	btQuaternion rot = ((btRigidBody*)self->btbody)->getWorldTransform().getRotation();
	PyObject* out = PyTuple_New(4);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(rot.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(rot.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(rot.getZ()));
	PyTuple_SetItem(out, 3, PyFloat_FromDouble(rot.getW()));
	return out;
}
int rigidbody_setrotation(rigidbody_obj* self, PyObject* value)
{
	btQuaternion q;
	if (!pyObjToVector(value, *((btVector3*)&q))) return NULL;
	btTransform& trans = ((btRigidBody*)self->btbody)->getWorldTransform();
	trans.setRotation(q);
	//if (world) world->GetWorld()->updateSingleAabb(object);
	return 0;
}

PyObject* rigidbody_getfriction(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getFriction());
}

int rigidbody_setfriction(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to friction.");
		return -1;
	}
	((btRigidBody*)self->btbody)->setFriction((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* rigidbody_getrestitution(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getRestitution());
}

int rigidbody_setrestitution(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to restitution.");
		return -1;
	}
	((btRigidBody*)self->btbody)->setRestitution((float)PyFloat_AsDouble(value));
	return 0;
}


PyObject* rigidbody_getshape(rigidbody_obj* self)
{
	auto btshape = ((btRigidBody*)self->btbody)->getCollisionShape();
	return (PyObject*)btshape->getUserPointer();
}

int rigidbody_setshape(rigidbody_obj* self, PyObject* value) 
{
	if (value->ob_type != &ShapeType) {
		PyErr_SetString(PyExc_TypeError, "Only igeBullet.shape can be assigned to shape .");
		return -1;
	}
	((btRigidBody*)self->btbody)->setCollisionShape((btCollisionShape*)(((shape_obj*)value)->btshape));
	return 0;
}

PyObject* rigidbody_getenableCollisionCallback(rigidbody_obj* self)
{
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	int f = (flag & btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK) ? true : false;
	return PyLong_FromLong(f);
}

int rigidbody_setenableCollisionCallback(rigidbody_obj* self, PyObject* value) 
{
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to enableCollisionCallback.");
		return -1;
	}
	int f = PyLong_AsLong(value);
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	if (f)	flag |= btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK;
	else	flag &= (~btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK);
	((btRigidBody*)self->btbody)->setCollisionFlags(flag);
	return 0;
}

PyObject* rigidbody_getenableContactResponse(rigidbody_obj* self)
{
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	int f = (flag & btCollisionObject::CF_NO_CONTACT_RESPONSE) ? false : true;
	return PyLong_FromLong(f);
}

int rigidbody_setenableContactResponse(rigidbody_obj* self, PyObject* value) 
{
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to enableContactResponse.");
		return -1;
	}
	int f = PyLong_AsLong(value);
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	if (!f)	flag |= btCollisionObject::CF_NO_CONTACT_RESPONSE;
	else	flag &= (~btCollisionObject::CF_NO_CONTACT_RESPONSE);
	((btRigidBody*)self->btbody)->setCollisionFlags(flag);
	return 0;
}

PyObject* rigidbody_getcollisionGroupBit(rigidbody_obj* self)
{
	return PyLong_FromLong(self->collisionGroup);
}

int rigidbody_setcollisionGroupBit(rigidbody_obj* self, PyObject* value) {
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to collisionGroupBit.");
		return -1;
	}
	self->collisionGroup = PyLong_AsLong(value);
	if (((btRigidBody*)self->btbody)->getBroadphaseHandle() != NULL)
		((btRigidBody*)self->btbody)->getBroadphaseHandle()->m_collisionFilterGroup = self->collisionGroup;

	return 0;
}

PyObject* rigidbody_getcollisionGroupMask(rigidbody_obj* self)
{
	return PyLong_FromLong(self->collisionMask);
}

int rigidbody_setcollisionGroupMask(rigidbody_obj* self, PyObject* value) {
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to collisionGroupMask.");
		return -1;
	}
	self->collisionMask = PyLong_AsLong(value);
	if (((btRigidBody*)self->btbody)->getBroadphaseHandle() != NULL)
		((btRigidBody*)self->btbody)->getBroadphaseHandle()->m_collisionFilterMask = self->collisionMask;

	return 0;

}

PyObject* rigidbody_getlinearDamping(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getLinearDamping());
}
int rigidbody_setlinearDamping(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to linearDamping.");
		return -1;
	}
	btScalar ld = (btScalar)PyFloat_AsDouble(value);
	btScalar ad = ((btRigidBody*)self->btbody)->getAngularDamping();
	((btRigidBody*)self->btbody)->setDamping(ld, ad);
	return 0;
}


PyObject* rigidbody_getangularDamping(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getAngularDamping());
}
int rigidbody_setangularDamping(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to angularDamping.");
		return -1;
	}
	btScalar ld = ((btRigidBody*)self->btbody)->getLinearDamping();
	btScalar ad = (btScalar)PyFloat_AsDouble(value);
	((btRigidBody*)self->btbody)->setDamping(ld, ad);
	return 0;
}


PyObject* rigidbody_getlinearVelocity(rigidbody_obj* self)
{
	const btVector3& vel = ((btRigidBody*)self->btbody)->getLinearVelocity();
	PyObject* out = PyTuple_New(3);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(vel.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(vel.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(vel.getZ()));
	return out;
}
int rigidbody_setlinearVelocity(rigidbody_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector((PyObject*)value, v)) return -1;
	((btRigidBody*)self->btbody)->setLinearVelocity(v);
	return 0;
}

PyObject* rigidbody_getangularVelocity(rigidbody_obj* self)
{
	const btVector3& vel = ((btRigidBody*)self->btbody)->getAngularVelocity();
	PyObject* out = PyTuple_New(3);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(vel.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(vel.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(vel.getZ()));
	return out;
}
int rigidbody_setangularVelocity(rigidbody_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector((PyObject*)value, v)) return -1;
	((btRigidBody*)self->btbody)->setAngularVelocity(v);
	return 0;
}


PyObject* rigidbody_getangularSleepingThreshold(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getAngularSleepingThreshold());
}
int rigidbody_setangularSleepingThreshold(rigidbody_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to angularSleepingThreshol.");
		return -1;
	}
	btScalar l = ((btRigidBody*)self->btbody)->getLinearSleepingThreshold();
	btScalar a = (btScalar)PyFloat_AsDouble(value);
	((btRigidBody*)self->btbody)->setSleepingThresholds(l, a);
	return 0;
}

PyObject* rigidbody_getlinearSleepingThreshold(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getLinearSleepingThreshold());
}
int rigidbody_setlinearSleepingThreshold(rigidbody_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to angularSleepingThreshol.");
		return -1;
	}
	btScalar l = (btScalar)PyFloat_AsDouble(value);
	btScalar a = ((btRigidBody*)self->btbody)->getAngularSleepingThreshold();
	((btRigidBody*)self->btbody)->setSleepingThresholds(l, a);
	return 0;
}

PyObject* rigidbody_getdeactivationTime(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getDeactivationTime());
}
int rigidbody_setdeactivationTime(rigidbody_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to deactivationTime.");
		return -1;
	}
	btScalar l = (btScalar)PyFloat_AsDouble(value);
	((btRigidBody*)self->btbody)->setDeactivationTime(l);
	return 0;
}

static PyObject* rigidbody_applyTorque(rigidbody_obj* self, PyObject* args) 
{
	PyObject* arg = nullptr;
	if (!PyArg_ParseTuple(args, "O", &arg)) {
		return NULL;
	}
	btVector3 v;
	if (!pyObjToVector(arg, v)) return NULL;
	((btRigidBody*)self->btbody)->applyTorque(v);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* rigidbody_applyForce(rigidbody_obj* self, PyObject* args)
{
	PyObject* arg1 = nullptr;
	PyObject* arg2 = nullptr;
	if (!PyArg_ParseTuple(args, "O|O", &arg1, &arg2)) {
		return NULL;
	}
	btVector3 v1;
	if (!pyObjToVector(arg1, v1)) return NULL;
	if (!arg2) {
		((btRigidBody*)self->btbody)->applyCentralForce(v1);
	}
	else {
		btVector3 v2;
		if (!pyObjToVector(arg2, v2)) return NULL;
		((btRigidBody*)self->btbody)->applyForce(v1, v2);
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* rigidbody_applyImpulse(rigidbody_obj* self, PyObject* args)
{
	PyObject* arg1 = nullptr;
	PyObject* arg2 = nullptr;
	if (!PyArg_ParseTuple(args, "O|O", &arg1, &arg2)) {
		return NULL;
	}
	btVector3 v1;
	if (!pyObjToVector(arg1, v1)) return NULL;

	if (!arg2) {
		((btRigidBody*)self->btbody)->applyCentralImpulse(v1);
	}
	else {
		btVector3 v2;
		if (!pyObjToVector(arg2, v2)) return NULL;
		((btRigidBody*)self->btbody)->applyImpulse(v1, v2);
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* rigidbody_clearForces(rigidbody_obj* self)
{
	((btRigidBody*)self->btbody)->clearForces();
	Py_INCREF(Py_None);
	return Py_None;
}


PyMethodDef rigidbody_methods[] = {
	{ "applyTorque", (PyCFunction)rigidbody_applyTorque, METH_VARARGS, applyTorque_doc},
	{ "applyForce", (PyCFunction)rigidbody_applyForce, METH_VARARGS, applyForce_doc},
	{ "applyImpulse", (PyCFunction)rigidbody_applyImpulse, METH_VARARGS, applyImpulse_doc},
	{ "clearForces", (PyCFunction)rigidbody_clearForces, METH_NOARGS, clearForces_doc},
	{ NULL,	NULL }
};

PyGetSetDef rigidbody_getsets[] = {
	{ const_cast<char*>("position"), (getter)rigidbody_getposition, (setter)rigidbody_setposition,rigidbody_position_doc, NULL },
	{ const_cast<char*>("rotation"), (getter)rigidbody_getrotation, (setter)rigidbody_setrotation,rigidbody_rotation_doc, NULL },
	{ const_cast<char*>("friction"), (getter)rigidbody_getfriction, (setter)rigidbody_setfriction,rigidbody_friction_doc, NULL },
	{ const_cast<char*>("restitution"), (getter)rigidbody_getrestitution, (setter)rigidbody_setrestitution,rigidbody_restitution_doc, NULL },
	{ const_cast<char*>("shape"), (getter)rigidbody_getshape, (setter)rigidbody_setshape, rigidbody_shape_doc, NULL },
	{ const_cast<char*>("enableCollisionCallback"), (getter)rigidbody_getenableCollisionCallback, (setter)rigidbody_setenableCollisionCallback, rigidbody_enableCollisionCallback_doc, NULL },
	{ const_cast<char*>("enableContactResponse"), (getter)rigidbody_getenableContactResponse, (setter)rigidbody_setenableContactResponse, rigidbody_enableContactResponse_doc, NULL },
	{ const_cast<char*>("collisionGroupBit"), (getter)rigidbody_getcollisionGroupBit, (setter)rigidbody_setcollisionGroupBit, rigidbody_collisionGroupBit_doc, NULL },
	{ const_cast<char*>("collisionGroupMask"), (getter)rigidbody_getcollisionGroupMask, (setter)rigidbody_setcollisionGroupMask, rigidbody_collisionGroupMask_doc, NULL },

	{ const_cast<char*>("linearDamping"), (getter)rigidbody_getlinearDamping, (setter)rigidbody_setlinearDamping, rigidbody_linearDamping_doc, NULL },
	{ const_cast<char*>("angularDamping"), (getter)rigidbody_getangularDamping, (setter)rigidbody_setangularDamping, rigidbody_angularDamping_doc, NULL },
	{ const_cast<char*>("linearVelocity"), (getter)rigidbody_getlinearVelocity, (setter)rigidbody_setlinearVelocity, rigidbody_linearVelocity_doc, NULL },
	{ const_cast<char*>("angularVelocity"), (getter)rigidbody_getangularVelocity, (setter)rigidbody_setangularVelocity, rigidbody_angularVelocity_doc, NULL },
	{ const_cast<char*>("angularSleepingThreshold"), (getter)rigidbody_getangularSleepingThreshold, (setter)rigidbody_setangularSleepingThreshold, rigidbody_angularSleepingThreshold_doc, NULL },
	{ const_cast<char*>("linearSleepingThreshold"), (getter)rigidbody_getlinearSleepingThreshold, (setter)rigidbody_setlinearSleepingThreshold, rigidbody_linearSleepingThreshold_doc, NULL },
	{ const_cast<char*>("deactivationTime"), (getter)rigidbody_getdeactivationTime, (setter)rigidbody_setdeactivationTime, rigidbody_deactivationTime_doc, NULL },
	{ NULL, NULL }
};




PyTypeObject RigidBodyType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.rigidBody",				/* tp_name */
	sizeof(rigidbody_obj),              /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)rigidbody_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)rigidbody_str,            /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	rigidbody_doc,						/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	rigidbody_methods,					/* tp_methods */
	0,                                  /* tp_members */
	rigidbody_getsets,                  /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	rigidbody_new,						/* tp_new */
	0,									/* tp_free */
};


#endif
//////////////////////////////////////////////////////////////////////
//World
//////////////////////////////////////////////////////////////////////
#if true
PyObject* dynworld_new(PyTypeObject* type, PyObject* args, PyObject* kw) {


	btBroadphaseInterface* broadphase = nullptr;
	btCollisionDispatcher* dispatcher = nullptr;
	btGhostPairCallback* ghostPairCallback = nullptr;
	btConstraintSolver* solver = nullptr;
	btDefaultCollisionConfiguration* collisionConfiguration = nullptr;
	btDiscreteDynamicsWorld* world = nullptr;

	///collision configuration contains default setup for memory, collision setup
	btDefaultCollisionConstructionInfo ci;
	//ci.m_defaultStackAllocatorSize = 256 * 1024;
	//ci.m_defaultMaxPersistentManifoldPoolSize = 512;
	//ci.m_defaultMaxCollisionAlgorithmPoolSize = 512;

	collisionConfiguration = new btDefaultCollisionConfiguration(ci);
	//collisionConfiguration->setConvexConvexMultipointIterations();

	///use the default collision dispatcher. For parallel processing you can use a diffent dispatcher (see Extras/BulletMultiThreaded)
	dispatcher = new btCollisionDispatcher(collisionConfiguration);

	//broadphase = _new btAxisSweep3(btVector3(-100,-10,-100),btVector3(100,10,100));
	broadphase = new btDbvtBroadphase();
	ghostPairCallback = new btGhostPairCallback();
	broadphase->getOverlappingPairCache()->setInternalGhostPairCallback(ghostPairCallback);

	solver = new btSequentialImpulseConstraintSolver;

	world = new btDiscreteDynamicsWorld(dispatcher,broadphase,solver,collisionConfiguration);
	btContactSolverInfo& info = world->getSolverInfo();
	info.m_numIterations = 4;


	world_obj* self = (world_obj*)type->tp_alloc(type, 0);
	self->broadphase = broadphase;
	self->dispatcher = dispatcher;
	self->solver = solver;
	self->ghostPairCallback = ghostPairCallback;
	self->collisionConfiguration = collisionConfiguration;
	self->btworld = world;


#if defined _WIN32
	QueryPerformanceFrequency((LARGE_INTEGER*) & (self->freq));
#elif defined __ANDROID__
#else
	mach_timebase_info(&base);
#endif
	return (PyObject*)self;
}

void  dynworld_dealloc(world_obj* self)
{
	for (int i = ((btDiscreteDynamicsWorld*)(self->btworld))->getNumCollisionObjects() - 1; i >= 0; i--){
		btCollisionObject* obj = ((btDiscreteDynamicsWorld*)(self->btworld))->getCollisionObjectArray()[i];
		rigidbody_obj* bodyobj = (rigidbody_obj*)obj->getUserPointer();
		Py_DECREF(bodyobj);
	}
	delete ((btDefaultCollisionConfiguration*)(self->collisionConfiguration));
	delete ((btCollisionDispatcher*)(self->dispatcher));
	delete ((btDbvtBroadphase*)(self->broadphase));
	delete ((btGhostPairCallback*)(self->ghostPairCallback));
	delete ((btSequentialImpulseConstraintSolver*)(self->solver));
	delete ((btDiscreteDynamicsWorld*)(self->btworld));
	Py_TYPE(self)->tp_free(self);
}

PyObject* dynworld_str(world_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics world object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* dynworld_add(world_obj* self, PyObject* args) {
	PyObject* obj;
	int disableCollisionsBetweenLinkedBodies = 0;
	if (!PyArg_ParseTuple(args, "O|p", &obj, &disableCollisionsBetweenLinkedBodies))return NULL;

	if (obj->ob_type == &RigidBodyType) {
		rigidbody_obj* bodyObj = (rigidbody_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->addRigidBody((btRigidBody*)(bodyObj->btbody), bodyObj->collisionGroup,bodyObj->collisionMask);
		Py_INCREF(obj);
	}
	else if (obj->ob_type == &ConstraintType) {
		constraint_obj* constraintObj = (constraint_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->addConstraint((btTypedConstraint*)constraintObj->btconstraint, disableCollisionsBetweenLinkedBodies);
		Py_INCREF(obj);
	}
	else {
		PyErr_SetString(PyExc_TypeError, "parameter error.");
		return NULL;
	}
	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* dynworld_remove(world_obj* self, PyObject* args) {
	PyObject* obj;
	if (!PyArg_ParseTuple(args, "O", &obj))return NULL;

	if (obj->ob_type == &RigidBodyType) {
		((btDiscreteDynamicsWorld*)self->btworld)->removeRigidBody((btRigidBody*)(((rigidbody_obj*)obj)->btbody));
		Py_DECREF(obj);
	}
	else if (obj->ob_type == &ConstraintType) {
		constraint_obj* constraintObj = (constraint_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->removeConstraint((btTypedConstraint*)constraintObj->btconstraint);
		Py_DECREF(obj);
	}
	else {
		PyErr_SetString(PyExc_TypeError, "parameter error.");
		return NULL;
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* dynworld_step(world_obj* self, PyObject* args) {

	double cpuTime;
#if defined _WIN32
	static LARGE_INTEGER	cuurentTime;
	QueryPerformanceCounter(&cuurentTime);
	LARGE_INTEGER* freq = (LARGE_INTEGER*) & (self->freq);
	cpuTime = (double)cuurentTime.QuadPart / (double)freq->QuadPart;
#elif defined __ANDROID__
	struct timespec tv;
	clock_gettime(CLOCK_MONOTONIC, &tv);
	cpuTime = (double)tv.tv_sec + (double)tv.tv_nsec / 1000000000.0;
#else
	uint64_t t = mach_absolute_time();
	cpuTime = (double)t * (double)base.numer / (double)base.denom / 1000000000.0;
#endif
	double elapsedTime = cpuTime - self->lasttime;
	self->lasttime = cpuTime;
	if (elapsedTime > 0.333333333333)elapsedTime = 0.333333333333;
	((btDiscreteDynamicsWorld*)self->btworld)->stepSimulation((btScalar)elapsedTime);

	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* dynworld_wait(world_obj* self) {
	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* dynworld_getgravity(world_obj* self)
{
	btVector3 vec = ((btDiscreteDynamicsWorld*)self->btworld)->getGravity();
	PyObject* out = PyTuple_New(3);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(vec.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(vec.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(vec.getZ()));
	return out;
}

int dynworld_setgravity(world_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector(value, v)) return -1;
	((btDiscreteDynamicsWorld*)self->btworld)->setGravity(v);
	return 0;
}

static PyObject* dynworld_clear(world_obj* self) {
	auto world = ((btDiscreteDynamicsWorld*)self->btworld);
	for (int i = world->getNumCollisionObjects() - 1; i >= 0; i--)
	{
		btCollisionObject* obj = world->getCollisionObjectArray()[i];
		world->removeCollisionObject(obj);
		PyObject* pyobj = (PyObject*)obj->getUserPointer();
		Py_DECREF(pyobj);
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* dynworld_getNumCollisionObjects(world_obj* self) {
	return PyLong_FromLong(((btDiscreteDynamicsWorld*)self->btworld)->getNumCollisionObjects());
}

static PyObject* dynworld_getRigidBody(world_obj* self, PyObject* args) {
	int index;
	if (!PyArg_ParseTuple(args, "i", &index))return NULL;
	btCollisionObject* obj = ((btDiscreteDynamicsWorld*)self->btworld)->getCollisionObjectArray()[index];
	return (PyObject*)obj->getUserPointer();
}


struct	MyClosestRayResultCallback : public btCollisionWorld::ClosestRayResultCallback
{
	int index;
	MyClosestRayResultCallback(const btVector3& rayFromWorld, const btVector3& rayToWorld)
		: ClosestRayResultCallback(rayFromWorld, rayToWorld)
		, index(0) {}
	virtual	btScalar addSingleResult(btCollisionWorld::LocalRayResult& rayResult, bool normalInWorldSpace) {
		if (rayResult.m_localShapeInfo) index = rayResult.m_localShapeInfo->m_triangleIndex;
		return ClosestRayResultCallback::addSingleResult(rayResult, normalInWorldSpace);
	}
};


static PyObject* dynworld_rayTestOne(world_obj* self, PyObject* args) 
{
	PyObject* startObj;
	PyObject* endObj;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "OO|ii", &startObj, &endObj, &mask, &group)) return NULL;

	btVector3 s, e;
	if (!pyObjToVector(startObj, s)) return NULL;
	if (!pyObjToVector(endObj, e)) return NULL;
	MyClosestRayResultCallback cb(s, e);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->rayTest(s, e, cb);
	if (!cb.hasHit()) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* outpos = PyTuple_New(3);
	if (!outpos) return NULL;
	PyTuple_SetItem(outpos, 0, PyFloat_FromDouble(cb.m_hitPointWorld.x()));
	PyTuple_SetItem(outpos, 1, PyFloat_FromDouble(cb.m_hitPointWorld.y()));
	PyTuple_SetItem(outpos, 2, PyFloat_FromDouble(cb.m_hitPointWorld.z()));
	PyObject* outnom = PyTuple_New(3);
	if (!outnom) return NULL;
	PyTuple_SetItem(outnom, 0, PyFloat_FromDouble(cb.m_hitNormalWorld.x()));
	PyTuple_SetItem(outnom, 1, PyFloat_FromDouble(cb.m_hitNormalWorld.y()));
	PyTuple_SetItem(outnom, 2, PyFloat_FromDouble(cb.m_hitNormalWorld.z()));

	PyObject* _res =
		Py_BuildValue(
			"{s:O,s:O,s:O,s:i}",
			"collisionObject", (PyObject*)((btCollisionObject*)cb.m_collisionObject->getUserPointer()),
			"hitPosition", outpos,
			"hitNormal", outnom,
			"index", cb.index);
	return _res;
}


struct	MyAllHitsRayResultCallback : public btCollisionWorld::AllHitsRayResultCallback
{
	btAlignedObjectArray<int> indices;
	MyAllHitsRayResultCallback(const btVector3& rayFromWorld, const btVector3& rayToWorld)
		: AllHitsRayResultCallback(rayFromWorld, rayToWorld) {}
	virtual	btScalar addSingleResult(btCollisionWorld::LocalRayResult& rayResult, bool normalInWorldSpace) {
		int index = 0;
		if (rayResult.m_localShapeInfo) index = rayResult.m_localShapeInfo->m_triangleIndex;
		indices.push_back(index);
		return AllHitsRayResultCallback::addSingleResult(rayResult, normalInWorldSpace);
	}
};

static PyObject* dynworld_rayTestAll(world_obj* self, PyObject* args) 
{
	PyObject* startObj;
	PyObject* endObj;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "OO|ii", &startObj, &endObj, &mask, &group))return NULL;

	btVector3 s, e;
	if (!pyObjToVector(startObj, s)) return NULL;
	if (!pyObjToVector(endObj, e)) return NULL;
	MyAllHitsRayResultCallback cb(s, e);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->rayTest(s, e, cb);
	if (!cb.hasHit()) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* out = PyTuple_New(cb.m_hitFractions.size());
	for (int i = 0; i < cb.m_hitFractions.size(); i++)
	{
		PyObject* outpos = PyTuple_New(3);
		if (!outpos) return NULL;
		PyTuple_SetItem(outpos, 0, PyFloat_FromDouble(cb.m_hitPointWorld[i].x()));
		PyTuple_SetItem(outpos, 1, PyFloat_FromDouble(cb.m_hitPointWorld[i].y()));
		PyTuple_SetItem(outpos, 2, PyFloat_FromDouble(cb.m_hitPointWorld[i].z()));
		PyObject* outnom = PyTuple_New(3);
		if (!outnom) return NULL;
		PyTuple_SetItem(outnom, 0, PyFloat_FromDouble(cb.m_hitNormalWorld[i].x()));
		PyTuple_SetItem(outnom, 1, PyFloat_FromDouble(cb.m_hitNormalWorld[i].y()));
		PyTuple_SetItem(outnom, 2, PyFloat_FromDouble(cb.m_hitNormalWorld[i].z()));
		PyObject* _res =
			Py_BuildValue(
				"{s:O,s:O,s:O,s:i}",
				"collisionObject", (PyObject*)((btCollisionObject*)cb.m_collisionObject->getUserPointer()),
				"hitPosition", outpos,
				"hitNormal", outnom,
				"index", cb.indices[i]);
		PyTuple_SetItem(out, i, _res);
	}
	return out;
}

struct ContactTestResult
{
	const btCollisionObject* objectA;
	const btCollisionObject* objectB;
	btVector3 localPosA;
	btVector3 localPosB;
	btVector3 worldPosA;
	btVector3 worldPosB;
	btVector3 normalB;
};
struct MyContactResultCallback : public btCollisionWorld::ContactResultCallback
{
	int count;
	std::vector<ContactTestResult>& outResults;
	MyContactResultCallback(std::vector<ContactTestResult>& _outResults)
		:ContactResultCallback(), outResults(_outResults), count(0) {}

	virtual btScalar addSingleResult(btManifoldPoint& cp, 
		const btCollisionObjectWrapper* colObj0Wrap, int partId0, int index0, 
		const btCollisionObjectWrapper* colObj1Wrap, int partId1, int index1){
		ContactTestResult result;
		result.objectA = colObj0Wrap->m_collisionObject;
		result.objectB = colObj1Wrap->m_collisionObject;
		result.worldPosA = cp.m_positionWorldOnA;
		result.worldPosB = cp.m_positionWorldOnB;
		result.localPosA = cp.m_localPointA;
		result.localPosB = cp.m_localPointB;
		result.normalB = cp.m_normalWorldOnB;
		outResults.push_back(result);
		count++;
		return 1.f;
	}
};


static PyObject* dynworld_contactTest(world_obj* self, PyObject* args) {
	///コリジョンテスト
	///特定のオブジェクトと他の全てのオブジェクトとの衝突判定
	///戻り				 : ヒット件数
	//int ContactTest(CollisionObject * colObj, std::vector<ContactTestResult> & outResults, short mask = -1, short group = 1);
	rigidbody_obj* obj;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "O|ii", &obj, &mask, &group))return NULL;
	if (obj->ob_base.ob_type != &RigidBodyType) {
		PyErr_SetString(PyExc_TypeError, "1st argument must be rigidBody.");
		return NULL;
	}
	std::vector<ContactTestResult> outResults;
	MyContactResultCallback cb(outResults);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->contactTest((btCollisionObject*)obj->btbody, cb);

	if (cb.count == 0) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* out = PyTuple_New(cb.count);
	int i = 0;
	for (auto it = outResults.begin(); it != outResults.end(); it++)
	{
		const btCollisionObject* objectA;
		const btCollisionObject* objectB;
		PyObject* localPosA = PyTuple_New(3);
		PyObject* localPosB = PyTuple_New(3);
		PyObject* worldPosA = PyTuple_New(3);
		PyObject* worldPosB = PyTuple_New(3);
		PyObject* normal = PyTuple_New(3);

		PyTuple_SetItem(localPosA, 0, PyFloat_FromDouble(it->localPosA.x()));
		PyTuple_SetItem(localPosA, 1, PyFloat_FromDouble(it->localPosA.y()));
		PyTuple_SetItem(localPosA, 2, PyFloat_FromDouble(it->localPosA.z()));
		PyTuple_SetItem(localPosB, 0, PyFloat_FromDouble(it->localPosB.x()));
		PyTuple_SetItem(localPosB, 1, PyFloat_FromDouble(it->localPosB.y()));
		PyTuple_SetItem(localPosB, 2, PyFloat_FromDouble(it->localPosB.z()));
		PyTuple_SetItem(worldPosA, 0, PyFloat_FromDouble(it->worldPosA.x()));
		PyTuple_SetItem(worldPosA, 1, PyFloat_FromDouble(it->worldPosA.y()));
		PyTuple_SetItem(worldPosA, 2, PyFloat_FromDouble(it->worldPosA.z()));
		PyTuple_SetItem(worldPosB, 0, PyFloat_FromDouble(it->worldPosB.x()));
		PyTuple_SetItem(worldPosB, 1, PyFloat_FromDouble(it->worldPosB.y()));
		PyTuple_SetItem(worldPosB, 2, PyFloat_FromDouble(it->worldPosB.z()));
		PyTuple_SetItem(normal, 0, PyFloat_FromDouble(it->normalB.x()));
		PyTuple_SetItem(normal, 1, PyFloat_FromDouble(it->normalB.y()));
		PyTuple_SetItem(normal, 2, PyFloat_FromDouble(it->normalB.z()));

		PyObject* _res =
			Py_BuildValue(
				"{s:O,s:O,s:O,s:O,s:O,s:O,s:O}",
				"objectA", (PyObject*)((btCollisionObject*)it->objectA->getUserPointer()),
				"objectB", (PyObject*)((btCollisionObject*)it->objectB->getUserPointer()),
				"localPosA", it->localPosA,
				"localPosB", it->localPosB,
				"worldPosA", it->worldPosA,
				"worldPosB", it->worldPosB,
				"normal", it->normalB);
		PyTuple_SetItem(out, i, _res);
		i++;
	}
	return out;
}

static PyObject* dynworld_contactPairTest(world_obj* self, PyObject* args) {
	///ペアコリジョンテスト
	///オブジェクト同士の衝突判定
	///戻り				 : ヒット件数
	//int ContactPairTest(CollisionObject * colObjA, CollisionObject * colObjB, std::vector<ContactTestResult> & outResults, short mask = -1, short group = 1);

	rigidbody_obj* objA;
	rigidbody_obj* objB;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "OO|ii", &objA, &objB, &mask, &group))return NULL;
	if (objA->ob_base.ob_type != &RigidBodyType || objB->ob_base.ob_type != &RigidBodyType) {
		PyErr_SetString(PyExc_TypeError, "1st,2nd argument must be rigidBody.");
		return NULL;
	}
	std::vector<ContactTestResult> outResults;
	MyContactResultCallback cb(outResults);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->contactPairTest((btCollisionObject*)objA->btbody, (btCollisionObject*)objB->btbody, cb);

	if (cb.count == 0) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* out = PyTuple_New(cb.count);
	int i = 0;
	for (auto it = outResults.begin(); it != outResults.end(); it++)
	{
		const btCollisionObject* objectA;
		const btCollisionObject* objectB;
		PyObject* localPosA = PyTuple_New(3);
		PyObject* localPosB = PyTuple_New(3);
		PyObject* worldPosA = PyTuple_New(3);
		PyObject* worldPosB = PyTuple_New(3);
		PyObject* normal = PyTuple_New(3);

		PyTuple_SetItem(localPosA, 0, PyFloat_FromDouble(it->localPosA.x()));
		PyTuple_SetItem(localPosA, 1, PyFloat_FromDouble(it->localPosA.y()));
		PyTuple_SetItem(localPosA, 2, PyFloat_FromDouble(it->localPosA.z()));
		PyTuple_SetItem(localPosB, 0, PyFloat_FromDouble(it->localPosB.x()));
		PyTuple_SetItem(localPosB, 1, PyFloat_FromDouble(it->localPosB.y()));
		PyTuple_SetItem(localPosB, 2, PyFloat_FromDouble(it->localPosB.z()));
		PyTuple_SetItem(worldPosA, 0, PyFloat_FromDouble(it->worldPosA.x()));
		PyTuple_SetItem(worldPosA, 1, PyFloat_FromDouble(it->worldPosA.y()));
		PyTuple_SetItem(worldPosA, 2, PyFloat_FromDouble(it->worldPosA.z()));
		PyTuple_SetItem(worldPosB, 0, PyFloat_FromDouble(it->worldPosB.x()));
		PyTuple_SetItem(worldPosB, 1, PyFloat_FromDouble(it->worldPosB.y()));
		PyTuple_SetItem(worldPosB, 2, PyFloat_FromDouble(it->worldPosB.z()));
		PyTuple_SetItem(normal, 0, PyFloat_FromDouble(it->normalB.x()));
		PyTuple_SetItem(normal, 1, PyFloat_FromDouble(it->normalB.y()));
		PyTuple_SetItem(normal, 2, PyFloat_FromDouble(it->normalB.z()));

		PyObject* _res =
			Py_BuildValue(
				"{s:O,s:O,s:O,s:O,s:O,s:O,s:O}",
				"objectA", (PyObject*)((btCollisionObject*)it->objectA->getUserPointer()),
				"objectB", (PyObject*)((btCollisionObject*)it->objectB->getUserPointer()),
				"localPosA", it->localPosA,
				"localPosB", it->localPosB,
				"worldPosA", it->worldPosA,
				"worldPosB", it->worldPosB,
				"normal", it->normalB);
		PyTuple_SetItem(out, i, _res);
		i++;
	}
	return out;
}

static PyObject* dynworld_convexSweepTest(world_obj* self, PyObject* args) {
	///シェイプ遷移テスト
	//int ConvexSweepTest(const CollisionShape * castShape, const Vector3 & fromPos, const Quat & fromRot, const Vector3 & tpPos, const Quat & toRot, short mask = -1);
	//void convexSweepTest (const btConvexShape* castShape, const btTransform& from, const btTransform& to, ConvexResultCallback& resultCallback,  btScalar allowedCcdPenetration = btScalar(0.)) const;
	return 0;

}

PyMethodDef dynworld_methods[] = {
	{ "add", (PyCFunction)dynworld_add, METH_VARARGS, add_doc},
	{ "remove", (PyCFunction)dynworld_remove, METH_VARARGS, remove_doc},
	{ "step", (PyCFunction)dynworld_step, METH_VARARGS, step_doc},
	{ "wait", (PyCFunction)dynworld_wait, METH_NOARGS, wait_doc},
	{ "clear", (PyCFunction)dynworld_clear, METH_NOARGS, clear_doc},
	{ "getNumCollisionObjects", (PyCFunction)dynworld_getNumCollisionObjects, METH_NOARGS, getNumCollisionObjects_doc},
	{ "getRigidBody", (PyCFunction)dynworld_getRigidBody, METH_VARARGS, getRigidBody_doc},
	{ "rayTestOne", (PyCFunction)dynworld_rayTestOne, METH_VARARGS, rayTestOne_doc},
	{ "rayTestAll", (PyCFunction)dynworld_rayTestAll, METH_VARARGS, rayTestAll_doc},
	{ "contactTest", (PyCFunction)dynworld_contactTest, METH_VARARGS, contactTest_doc},
	{ "contactPairTest", (PyCFunction)dynworld_contactPairTest, METH_VARARGS, contactPairTest_doc},
	//{ "convexSweepTest", (PyCFunction)dynworld_convexSweepTest, METH_VARARGS, convexSweepTest_doc},
	{ NULL,	NULL }
};

PyGetSetDef dynworld_getsets[] = {
	{ const_cast<char*>("gravity"), (getter)dynworld_getgravity, (setter)dynworld_setgravity,gravity_doc, NULL },
	{ NULL, NULL }
};

PyTypeObject DynamicsWorldType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.world",					/* tp_name */
	sizeof(world_obj),					/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)dynworld_dealloc,			/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)dynworld_str,			   /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	dynworld_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	dynworld_methods,						/* tp_methods */
	0,                                  /* tp_members */
	dynworld_getsets,				      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	dynworld_new,							/* tp_new */
	0,									/* tp_free */
};

#endif

//////////////////////////////////////////////////////////////////////
//pyxBullet
//////////////////////////////////////////////////////////////////////
static PyMethodDef pyxBullet_methods[] = {
{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef igeBullet_module = {
	PyModuleDef_HEAD_INIT,
	"igeBullet",								// Module name to use with Python import statements
	"Bullet wrapper for pyxie game engine.",	// Module description
	0,
	pyxBullet_methods							// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeBullet() {
	PyObject* module = PyModule_Create(&igeBullet_module);


	PyObject* vmathmod = PyImport_ImportModule("igeVmath");
	if (!vmathmod) return NULL;
	Vec2Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "vec2");
	Vec3Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "vec3");
	Vec4Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "vec4");
	QuatType = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "quat");
	Mat22Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "mat22");
	Mat33Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "mat33");
	Mat44Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "mat44");
	Py_DECREF(vmathmod);

	if (PyType_Ready(&ShapeType) < 0) return NULL;
	if (PyType_Ready(&RigidBodyType) < 0) return NULL;
	if (PyType_Ready(&DynamicsWorldType) < 0) return NULL;
	if (PyType_Ready(&ConstraintType) < 0) return NULL;

	Py_INCREF(&ShapeType);
	PyModule_AddObject(module, "shape", (PyObject*)& ShapeType);
	Py_INCREF(&RigidBodyType);
	PyModule_AddObject(module, "rigidBody", (PyObject*)& RigidBodyType);
	Py_INCREF(&DynamicsWorldType);
	PyModule_AddObject(module, "world", (PyObject*)& DynamicsWorldType);
	Py_INCREF(&ConstraintType);
	PyModule_AddObject(module, "constraint", (PyObject*)& ConstraintType);

	PyModule_AddIntConstant(module, "BOX_SHAPE_PROXYTYPE", BOX_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "SPHERE_SHAPE_PROXYTYPE", SPHERE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CAPSULE_SHAPE_PROXYTYPE", CAPSULE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CONE_SHAPE_PROXYTYPE", CONE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CYLINDER_SHAPE_PROXYTYPE", CYLINDER_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "STATIC_PLANE_PROXYTYPE", STATIC_PLANE_PROXYTYPE);
	PyModule_AddIntConstant(module, "COMPOUND_SHAPE_PROXYTYPE", COMPOUND_SHAPE_PROXYTYPE);

	PyModule_AddIntConstant(module, "RO_XYZ", RO_XYZ);
	PyModule_AddIntConstant(module, "RO_XZY", RO_XZY);
	PyModule_AddIntConstant(module, "RO_YXZ", RO_YXZ);
	PyModule_AddIntConstant(module, "RO_YZX", RO_YZX);
	PyModule_AddIntConstant(module, "RO_ZXY", RO_ZXY);
	PyModule_AddIntConstant(module, "RO_ZYX", RO_ZYX);

	PyModule_AddIntConstant(module, "POINT2POINT_CONSTRAINT_TYPE", POINT2POINT_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "HINGE_CONSTRAINT_TYPE", HINGE_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "CONETWIST_CONSTRAINT_TYPE", CONETWIST_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "D6_CONSTRAINT_TYPE", D6_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "SLIDER_CONSTRAINT_TYPE", SLIDER_CONSTRAINT_TYPE);
	//PyModule_AddIntConstant(module, "CONTACT_CONSTRAINT_TYPE", CONTACT_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "D6_SPRING_CONSTRAINT_TYPE", D6_SPRING_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "GEAR_CONSTRAINT_TYPE", GEAR_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "FIXED_CONSTRAINT_TYPE", FIXED_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "D6_SPRING_2_CONSTRAINT_TYPE", D6_SPRING_2_CONSTRAINT_TYPE);

	return module;
}
