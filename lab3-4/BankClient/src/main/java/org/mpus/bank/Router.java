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
                System.out.println(is.readLong());
            }

            is.endEncapsulation();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void addAccount(String owner) {
        OutputStream os = new OutputStream(communicator);
        try {
            os.startEncapsulation();
            os.writeString(owner);
            os.endEncapsulation();

            Ice_invokeResult result = base.ice_invoke("addAccount", OperationMode.Normal, os.finished());
            if (result.returnValue) {
                System.out.println("Account created");
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
        String exceptionId = is.readString();

        if (exceptionId.equals("::Bank::AccountNotFound")) {
            System.out.println("Account not found: " + is.readString());
        }
        else if (exceptionId.equals("::Bank::AccountAlreadyExists")) {
            System.out.println("Account already exists: " + is.readString());
        }
        else if (exceptionId.equals("::Bank::InvalidAmount")) {
            System.out.println("Invalid amount: " + is.readLong());
        }
        else if (exceptionId.equals("::Bank::InsufficientFunds")) {
            System.out.println("Insufficient funds on: " + is.readString());
            System.out.println("Amount: " + is.readString());
        }

        is.endEncapsulation();
    }
}
