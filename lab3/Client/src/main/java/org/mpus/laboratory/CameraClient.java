package org.mpus.laboratory;

import io.grpc.ManagedChannel;
import io.grpc.StatusRuntimeException;

public class CameraClient {
    private final CameraServiceGrpc.CameraServiceBlockingStub stub;

    public CameraClient(ManagedChannel channel) {
        stub = CameraServiceGrpc.newBlockingStub(channel);
    }

    public void getCameraStatus(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            CameraStatus response = stub.getCameraStatus(request);
            System.out.println("Camera status:");
            System.out.println("ID: " + response.getId().getId());
            System.out.println("Power: " + response.getIsOn());
            System.out.println("Pan: " + response.getPan());
            System.out.println("Tilt: " + response.getTilt());
            System.out.println("Zoom: " + response.getZoom());
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void enableCamera(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            stub.enableCamera(request);
            System.out.println("Camera " + id + " enabled");
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void disableCamera(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            stub.disableCamera(request);
            System.out.println("Camera " + id + " disabled");
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setPan(String id, String pan) {
        int panVal;
        try {
            panVal = Integer.parseInt(pan);
        } catch (NumberFormatException e) {
            System.out.println("Invalid pan value");
            return;
        }

        if (panVal < 0 || panVal > 359) {
            System.out.println("Pan value must be between 0-359");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetCameraPanRequest request = SetCameraPanRequest.newBuilder()
                .setId(deviceID).setPan(panVal).build();
        try {
            stub.setCameraPan(request);
            System.out.println("Set camera " + id + " pan to " + panVal);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setTilt(String id, String tilt) {
        int tiltVal;
        try {
            tiltVal = Integer.parseInt(tilt);
        } catch (NumberFormatException e) {
            System.out.println("Invalid tilt value");
            return;
        }

        if (tiltVal < 0 || tiltVal > 180) {
            System.out.println("Tilt value must be between 0-180");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetCameraTiltRequest request = SetCameraTiltRequest.newBuilder()
                .setId(deviceID).setTilt(tiltVal).build();
        try {
            stub.setCameraTilt(request);
            System.out.println("Set camera " + id + " tilt to " + tiltVal);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setZoom(String id, String zoom) {
        int zoomVal;
        try {
            zoomVal = Integer.parseInt(zoom);
        } catch (NumberFormatException e) {
            System.out.println("Invalid zoom value");
            return;
        }

        if (zoomVal < 1 || zoomVal > 20) {
            System.out.println("Zoom value must be between 1-20");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetCameraZoomRequest request = SetCameraZoomRequest.newBuilder()
                .setId(deviceID).setZoom(zoomVal).build();
        try {
            stub.setCameraZoom(request);
            System.out.println("Set camera " + id + " zoom to " + zoomVal);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }
}
