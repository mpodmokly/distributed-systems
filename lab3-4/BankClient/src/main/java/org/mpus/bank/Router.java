package org.mpus.bank;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Object.Ice_invokeResult;

import java.lang.Exception;

public class Router {
    private Communicator communicator;
    private ObjectPrx base;

    public Router(String[] args) {
        try {
            communicator = Util.initialize(args);
            base = communicator.stringToProxy("service:default -p 10000");
        } catch (Exception e) {
            e.printStackTrace();
            shutdown();
        }
    }

    public void list() {
        try {
            Ice_invokeResult result = base.ice_invoke("listAccounts", OperationMode.Normal, null);
            InputStream is = new InputStream(communicator, result.outParams);
            is.startEncapsulation();

            int size = is.readSize();
            for (int i = 0; i < size; i++) {
                System.out.print(is.readString() + " ");
                System.out.println((double) is.readLong() / 100);
            }

            is.endEncapsulation();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void getBalance(String owner) {
        OutputStream os = new OutputStream(communicator);
        try {
            os.startEncapsulation();
            os.writeString(owner);
            os.endEncapsulation();

            Ice_invokeResult result = base.ice_invoke("getBalance", OperationMode.Normal, os.finished());
            if (result.returnValue) {
                InputStream is = new InputStream(communicator, result.outParams);
                is.startEncapsulation();
                System.out.println("Balance: " + (double) is.readLong() / 100);
                is.endEncapsulation();
            }
            else {
                handleException(result);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void manageAccount(String command, String owner) {
        String methodName = command + "Account";

        OutputStream os = new OutputStream(communicator);
        try {
            os.startEncapsulation();
            os.writeString(owner);
            os.endEncapsulation();

            Ice_invokeResult result = base.ice_invoke(methodName, OperationMode.Normal, os.finished());
            if (result.returnValue) {
                System.out.print("Account ");
                if (command.equals("add")) {
                    System.out.println("created");
                }
                else {
                    System.out.println("deleted");
                }
            }
            else {
                handleException(result);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void manageMoney(String command, String owner, String amount) {
        long amountVal;
        try {
            amountVal = Long.parseLong(amount);
        } catch (NumberFormatException e) {
            System.out.println("Invalid amount");
            return;
        }

        OutputStream os = new OutputStream(communicator);
        try {
            os.startEncapsulation();
            os.writeString(owner);
            os.writeLong(amountVal * 100);
            os.endEncapsulation();

            Ice_invokeResult result = base.ice_invoke(command, OperationMode.Normal, os.finished());
            if (result.returnValue) {
                System.out.println("Amount deposited");
            }
            else {
                handleException(result);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void shutdown() {
        if (communicator != null) {
            communicator.destroy();
        }
    }

    private void handleException(Ice_invokeResult result) {
        InputStream is = new InputStream(communicator, result.outParams);
        is.startEncapsulation();

        is.readByte();
        String[] exceptionNameSplit = is.readString().split(":");
        String exceptionId = exceptionNameSplit[exceptionNameSplit.length - 1];

        switch (exceptionId) {
            case "AccountNotFound" -> System.out.println("Account not found: " + is.readString());
            case "AccountAlreadyExists" -> System.out.println("Account already exists: " + is.readString());
            case "InvalidAmount" -> System.out.println("Invalid amount: " + (double) is.readLong() / 100);
            case "InsufficientFunds" -> {
                System.out.println("Insufficient funds on: " + is.readString());
                System.out.println("Amount: " + (double) is.readLong() / 100);
                System.out.println("Available: " + (double) is.readLong() / 100);
            }
        }

        is.endEncapsulation();
    }
}
