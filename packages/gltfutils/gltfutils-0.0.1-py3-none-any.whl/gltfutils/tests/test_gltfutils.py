import unittest
import gltfutils
import os
import json


class TestElement(unittest.TestCase):
	DEFAULT_JSON = {}

	def assertEqualDefaultJson(self, data):
		self.assertEqual(data, self.DEFAULT_JSON)

	def assertEqualDefault(self, element):
		self.assertEqual(element.extensions, None)
		self.assertEqual(element.extras, None)


class TestMaterial(TestElement):
	pass


class TestBuffer(TestElement):
	pass


class TestBufferView(TestElement):
	pass


class TestAccessor(TestElement):
	pass


class TestScene(TestElement):
	def assertEqualDefault(self, scene):
		self.assertEqual(scene.nodes, [])
		self.assertEqual(scene.name, None)
		super().assertEqualDefault(scene)

	def test_default_constructor(self):
		self.assertEqualDefault(gltfutils.Scene())

	def test_serialize_default(self):
		self.assertEqualDefaultJson(gltfutils.to_json(gltfutils.Scene()))

	def test_from_json_default(self):
		self.assertEqualDefault(gltfutils.Scene.from_json(self.DEFAULT_JSON))

	def test_name_constructor(self):
		scene = gltfutils.Scene(name="test")
		self.assertEqual(scene.name, "test")

	def test_name_to_json(self):
		scene = gltfutils.Scene(name="test")
		self.assertEqual(gltfutils.to_json(scene), {"name":"test"})


class TestNode(TestElement):
	DEFAULT_JSON = {}
	
	def assertEqualDefault(self, node):
		self.assertEqual(node.name, None)
		self.assertEqual(node.matrix, (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0))
		self.assertEqual(node.translation, (0.0, 0.0, 0.0))
		self.assertEqual(node.rotation, (0.0, 0.0, 0.0, 1.0))
		self.assertEqual(node.scale, (1.0, 1.0, 1.0))
		self.assertEqual(node.mesh, None)
		self.assertEqual(node.camera, None)

		super().assertEqualDefault(node)

	def test_default_constructor(self):
		self.assertEqualDefault(gltfutils.Node())

	def test_default_to_json(self):
		self.assertEqualDefaultJson(gltfutils.to_json(gltfutils.Node()))

	def test_default_from_json(self):
		self.assertEqualDefault(gltfutils.Node.from_json(self.DEFAULT_JSON))


class TestAsset(TestElement):
	DEFAULT_JSON = {"version": "2.0"}

	def assertEqualDefault(self, asset):
		self.assertEqual(asset.version, "2.0")
		super().assertEqualDefault(asset)

	def test_default_constructor(self):
		self.assertEqualDefault(gltfutils.Asset())

	def test_default_constructor_to_json(self):
		self.assertEqualDefaultJson(gltfutils.to_json(gltfutils.Asset()))

	def test_from_json_default(self):
		self.assertEqualDefault(gltfutils.Asset.from_json(self.DEFAULT_JSON))

	def test_from_json_error_on_missing_version(self):
		with self.assertRaises(ValueError):
			asset = gltfutils.Asset.from_json({})

	def test_constructor(self):
		asset = gltfutils.Asset(
			version="2.1",
			generator="gltfutils 0.0.1",
			minVersion="2.0",
			extensions={"fake_extension_data":"something"},
			extras={"fake_extra_data":"extension_data"}
		)

		self.assertEqual(asset.version, "2.1")
		self.assertEqual(asset.generator, "gltfutils 0.0.1")
		self.assertEqual(asset.minVersion, "2.0")
		self.assertEqual(asset.extensions, {"fake_extension_data":"something"})
		self.assertEqual(asset.extras, {"fake_extra_data":"extension_data"})

	def test_constructor_to_json(self):
		asset = gltfutils.Asset(
			version="2.1",
			generator="gltfutils 0.0.1",
			minVersion="2.0",
			extensions={"fake_extension_data":"something"},
			extras={"fake_extra_data":"extension_data"}
		)

		self.assertEqual(gltfutils.to_json(asset), {
			"version": "2.1",
			"generator": "gltfutils 0.0.1",
			"minVersion": "2.0",
			"extensions": {"fake_extension_data":"something"},
			"extras": {"fake_extra_data":"extension_data"}
		})


class TestGLTF2(TestElement):
	DEFAULT_JSON = {'asset':{'version':'2.0'}}

	def assertEqualDefault(self, gltf):
		self.assertEqual(gltf.asset, gltfutils.Asset())
		super().assertEqualDefault(gltf)

	def test_default_constructor(self):
		self.assertEqualDefault(gltfutils.GLTF2())

	def test_default_constructor_to_json(self):
		gltf = gltfutils.GLTF2()
		self.assertEqualDefaultJson(gltfutils.to_json(gltf))

	def test_default_from_json(self):
		self.assertEqualDefault(gltfutils.GLTF2.from_json(self.DEFAULT_JSON))

	def test_from_json(self):
		data = {
			"asset": {
				"version": "2.0"
			},
			"nodes": [
				{
					"name": "node0"
				}
			],
			"scenes": [
				{
					"name": "scene0",
					"nodes": [0]
				}
			],
			"materials": [
			],
			"accessors": [
			],
			"bufferView":[
			],
			"buffers": [
			],
			"meshes":[
			]
		}

		gltf = gltfutils.GLTF2.from_json(data)

		self.assertEqual(gltf.asset.version, "2.0")
		self.assertEqual(gltf.nodes[0].name, "node0")
		self.assertEqual(gltf.scenes[0].name, "scene0")
		self.assertEqual(gltf.scenes[0].nodes, [0])

	def test_to_json(self):
		data = {
			"asset": {
				"version": "2.0"
			},
			"nodes": [
				{
					"name": "node0"
				}
			],
			"scenes": [
				{
					"name": "scene0",
					"nodes": [0]
				}
			]
		}

		gltf = gltfutils.GLTF2.from_json(data)

		result = gltfutils.to_json(gltf)

		self.assertEqual(data, result)


if __name__ == "__main__":
	unittest.main()
	
