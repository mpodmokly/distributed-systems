package org.mpus.laboratory;

import com.google.protobuf.Empty;
import io.grpc.ManagedChannel;

import java.util.List;

public class DeviceRegistryClient {
    private final DeviceRegistryServiceGrpc.DeviceRegistryServiceBlockingStub stub;

    public DeviceRegistryClient(ManagedChannel channel) {
        stub = DeviceRegistryServiceGrpc.newBlockingStub(channel);
    }

    public List<String> getDevices() {
        return stub.listDevices(Empty.getDefaultInstance())
                .getDevicesList()
                .stream()
                .map(DeviceID::getId)
                .toList();
    }
}
