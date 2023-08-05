
/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(shape_doc,
	"3d physics shape\n"\
	"\n"\
	"create box shape\n"\
	"shape = igeBullet.shape(igeBullet.BOX_SHAPE_PROXYTYPE, halfExtents = (1, 1, 1))\n"\
	"create sphere shape\n"\
	"shape = igeBullet.shape(igeBullet.SPHERE_SHAPE_PROXYTYPE, radius = 1)\n"\
	"create capsule shape\n"\
	"shape = igeBullet.shape(igeBullet.CAPSULE_SHAPE_PROXYTYPE, radius = 1, height = 1)\n"\
	"create cone shape\n"\
	"shape = igeBullet.shape(igeBullet.CONE_SHAPE_PROXYTYPE, radius = 1, height = 1)\n"\
	"create cylinder shape\n"\
	"shape = igeBullet.shape(igeBullet.CYLINDER_SHAPE_PROXYTYPE, halfExtents = (x, y, z))\n"\
	"create static plane shape\n"\
	"shape = igeBullet.shape(igeBullet.STATIC_PLANE_PROXYTYPE, normal = (x, y, z), constant = 1)\n"\
	"create compound shape\n"\
	"shape = igeBullet.shape(igeBullet.COMPOUND_SHAPE_PROXYTYPE)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    type\n"\
	"        shape type\n"\
	"        igeBullet.BOX_SHAPE_PROXYTYPE : box shape\n"\
	"        igeBullet.SPHERE_SHAPE_PROXYTYPE : sphere shape\n"\
	"        igeBullet.CAPSULE_SHAPE_PROXYTYPE : capsule shape\n"\
	"        igeBullet.CONE_SHAPE_PROXYTYPE : cone shape\n"\
	"        igeBullet.CYLINDER_SHAPE_PROXYTYPE : cylinder shape\n"\
	"        igeBullet.STATIC_PLANE_PROXYTYPE static plane shape\n"\
	"        igeBullet.COMPOUND_SHAPE_PROXYTYPE compound shape\n"\
	"    radius\n"\
	"        radius of sphere or capsule or cone\n"\
	"    height\n"\
	"        height of capsule or cone\n"\
	"    halfExtents\n"\
	"        half length of each side x,y,z\n"\
	"    normal\n"\
	"        normal of plane\n"\
	"    constant\n"\
	"        plane position along normal");

PyDoc_STRVAR(getMeshData_doc,
	"get rendering data\n"\
	"\n"\
	"pos, nom, uv, idx = shape.getMeshData()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    pos\n"\
	"        list of vertex positions (x,y,z, x,y,z, ...)\n"\
	"    pos\n"\
	"        list of vertex normals (x,y,z, x,y,z, ...)\n"\
	"    uv\n"\
	"        list of vertex uvs (u,v, u,v, ...)\n"\
	"    uv\n"\
	"        list of triangle indices\n");

/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(rigidbody_doc,
	"3d physics rigid body\n"\
	"\n"\
	"igeBullet.rigidBody(shape, mass, pos, rot, activate)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    shape : igeBullet.shape\n"\
	"        shape object\n"\
	"    mass : float\n"\
	"        mass of object\n"\
	"    pos : tuple of float (x,y,z)\n"\
	"        start location of object\n"\
	"    rot : tuple of float (x,y,z,w)\n"\
	"        start orientation of object\n"\
	"    activate : bool\n"\
	"        Whether the physics calculation is active.\n"\
	"        Do not calculate unless external force is applied\n");

PyDoc_STRVAR(rigidbody_position_doc,
	"rigit body position\n"\
	"\n"\
	"    type :  tuple(x,y,z)\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_rotation_doc,
	"rigit body position\n"\
	"\n"\
	"    type :  tuple(x,y,z,w)\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_friction_doc,
	"rigit body friction\n"\
	"\n"\
	"    type :  float\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_restitution_doc,
	"rigit body restitution\n"\
	"\n"\
	"    type :  float\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_shape_doc,
	"shape object\n"\
	"\n"\
	"    type :  igeBullet.shape\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_enableCollisionCallback_doc,
	"Whether collision callback is enabled\n"\
	"\n"\
	"    type :  bool\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_enableContactResponse_doc,
	"Whether contact response is enabled\n"\
	"\n"\
	"    type :  bool\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_collisionGroupBit_doc,
	"Own collision filter bit\n"\
	"\n"\
	"    type :  tuple(x,y,z)\n"\
	"   （1, 2, 4, 8, 16...16384）\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_collisionGroupMask_doc,
	"Collision filter bit for which you want to enable collision\n"\
	"\n"\
	"    type :  tuple(x,y,z)\n"\
	"   （1, 2, 4, 8, 16...16384）\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_linearDamping_doc,
	"rigid body linear damping\n"\
	"\n"\
	"    type :  float\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_angularDamping_doc,
	"rigid body angular damping\n"\
	"\n"\
	"    type :  float\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_linearVelocity_doc,
	"rigid body linear velocity\n"\
	"\n"\
	"    type :  tuple(x,y,z)\n"\
	"    read / write");

PyDoc_STRVAR(rigidbody_angularVelocity_doc,
	"rigid body angular velocity\n"\
	"\n"\
	"    type :  tuple(x,y,z)\n"\
	"    read / write");

PyDoc_STRVAR(applyTorque_doc,
	" Applies a torque on a rigid body.\n"\
	"\n"\
	"digidBody.applyTorque(torque)"
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    torque : tuple(x,y,z)\n");

PyDoc_STRVAR(applyForce_doc,
	"Applies a force on a rigid body.\n"\
	"If position is not specified, force is applied to the center.\n"\
	"\n"\
	"digidBody.applyForce(torque, position)"
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    force : tuple(x,y,z)\n"\
	"    position : tuple(x,y,z)  (optional)\n");

PyDoc_STRVAR(applyImpulse_doc,
	" Applies a impulse on a rigid body.\n"\
	"If position is not specified, force is applied to the center.\n"\
	"\n"\
	"digidBody.applyImpulse(impulse)"
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    impulse : tuple(x,y,z)\n"\
	"    position : tuple(x,y,z)  (optional)\n");

PyDoc_STRVAR(clearForces_doc,
	"The forces on each rigidbody is accumulating together with gravity.\n"\
	"clear this after each timestep.\n"\
	"\n"\
	"digidBody.clearForces()");



/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(dynworld_doc,
	"3d physics world\n");

PyDoc_STRVAR(gravity_doc,
	"gravity vector\n"\
	"\n"\
	"    type :  tuple(x,y,z)\n"\
	"    read / write");


PyDoc_STRVAR(add_doc,
	"Add rigidbody or constarain to world\n"\
	"\n"\
	"world.add(object)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    object : rigidBody or constrain\n"\
	"        rigidBody or constrain objecrt add to world.");

PyDoc_STRVAR(remove_doc,
	"Remove rigidbody or constarain from world\n"\
	"\n"\
	"world.remove(object)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    object : rigidBody or constrain\n"\
	"        rigidBody or constrain objecrt remove from world.");

PyDoc_STRVAR(clear_doc,
	"Clear all added rigidbody and constarain\n"\
	"\n"\
	"world.clear()\n"\
	"\n");

PyDoc_STRVAR(step_doc,
	"step simulation\n"\
	"\n"\
	"world.step()\n"\
	"\n");

PyDoc_STRVAR(wait_doc,
	"wait until async simultion is end\n"\
	"\n"\
	"world.wait()\n"\
	"\n");


PyDoc_STRVAR(getNumCollisionObjects_doc,
	"get number of collision objects in the world\n"\
	"\n"\
	"num = world.getNumCollisionObjects()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    num : int\n"\
	"        number of collision objects");


PyDoc_STRVAR(getRigidBody_doc,
	"get collision object\n"\
	"\n"\
	"obj = world.getRigidBody(index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    index : int\n"\
	"        index of added rigidBody(Order added)\n"\
	"Returns\n"\
	"-------\n"\
	"    obj : rigidBody\n"\
	"        rigidBody object");

