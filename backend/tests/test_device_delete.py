import unittest

from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine, select

from backend.api.devices import delete_device
from backend.models import Device


class DeviceDeleteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self) -> None:
        self.session.close()

    def _add_device(self, serial: str, status: str) -> Device:
        device = Device(serial=serial, platform="android", model="Pixel", status=status)
        self.session.add(device)
        self.session.commit()
        self.session.refresh(device)
        return device

    def test_delete_offline_device_removes_record(self):
        self._add_device("android-offline-1", "OFFLINE")

        payload = delete_device("android-offline-1", session=self.session)

        self.assertEqual(payload["message"], "设备 android-offline-1 已删除")
        deleted = self.session.exec(
            select(Device).where(Device.serial == "android-offline-1")
        ).first()
        self.assertIsNone(deleted)

    def test_delete_online_device_is_rejected(self):
        self._add_device("android-idle-1", "IDLE")

        with self.assertRaises(HTTPException) as context:
            delete_device("android-idle-1", session=self.session)

        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("仅离线设备支持删除", str(context.exception.detail))

        existing = self.session.exec(
            select(Device).where(Device.serial == "android-idle-1")
        ).first()
        self.assertIsNotNone(existing)

    def test_delete_missing_device_returns_404(self):
        with self.assertRaises(HTTPException) as context:
            delete_device("missing-device", session=self.session)

        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("设备不存在", str(context.exception.detail))


if __name__ == "__main__":
    unittest.main()
